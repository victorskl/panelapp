import requests
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, SimpleCookie
from jose import jwt

from accounts.models import Reviewer
from accounts.tasks import reviewer_confirmation_requset_email
from panelapp.settings import aws
from panelapp.settings.aws import AWS_ALB_SESSION_COOKIE_PREFIX


class ALBAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_holder = {}

    def __call__(self, request):
        self.process_login(request)
        return self.logout_cognito_user(request, self.get_response(request))

    def process_login(self, request):
        """
        Process login data when AMZN_OIDC_HEADERS presents. Verify JWT and extract claims for user information.

        :param request:
        :return:
        """
        meta = request.META
        if not self.has_amzn_oidc_headers(meta):
            return

        encoded_jwt_data = meta.get(aws.AMZN_OIDC_DATA)

        if self.verify_amzn_jwt_structure(encoded_jwt_data):

            public_key = self.get_public_key(encoded_jwt_data)

            claims = self.get_verified_jwt_claims(encoded_jwt_data, public_key)

            if claims is not None:
                email = claims.get("email")
                if email is None:
                    raise ValueError("JWT claims must contain email field", claims)

                first_name = claims.get("given_name", "")
                last_name = claims.get("family_name", "")

                self.login_cognito_user(request, email, first_name, last_name)
            else:
                self._remove_invalid_user(request)

    def login_cognito_user(self, request, email, first_name, last_name):
        """
        This will authenticate pass in user using email as username and set mandatory fields first_name and last_name.
        It will use Django RemoteUserBackend to facilitate creation of a new user if none exist before.
        Additionally, it will create PanelApp specific Reviewer and send email to curators for a new
        reviewer sign up email workflow. And put this new user to Reviewer.TYPES.EXTERNAL.

        :param request:
        :param email:
        :param first_name:
        :param last_name:
        :return:
        """
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated:
            if request.user.get_username() == self.clean_username(email, request):
                return
            else:
                # An authenticated user is associated with the request, but
                # it does not match the authorized user in the header.
                self._remove_invalid_user(request)

        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user using RemoteUserBackend and create if new
        user = auth.authenticate(request, remote_user=email)

        if user:
            # update required user attributes
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # create a reviewer profile if None exist before
            try:
                user.reviewer
            except ObjectDoesNotExist:
                Reviewer.objects.create(
                    user=user,
                    user_type=Reviewer.TYPES.EXTERNAL,
                    affiliation="Other",
                    role=Reviewer.ROLES.Other,
                    workplace=Reviewer.WORKPLACES.Other,
                    group=Reviewer.GROUPS.Other,
                )

                # send an email to PanelApp curators to check the new user
                reviewer_confirmation_requset_email.delay(user.pk)

            # User is valid. Set request.user and persist user in the session by logging the user in.
            request.user = user
            auth.login(request, user)

    @staticmethod
    def clean_username(username, request):
        """
        Allow the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError:  # Backend has no clean_username method.
            pass
        return username

    @staticmethod
    def _remove_invalid_user(request):
        """
        Remove the current authenticated user in the request which is invalid
        but only if the user is authenticated via the RemoteUserBackend.
        """
        try:
            stored_backend = load_backend(request.session.get(auth.BACKEND_SESSION_KEY, ''))
        except ImportError:
            # backend failed to load
            auth.logout(request)
        else:
            if isinstance(stored_backend, RemoteUserBackend):
                auth.logout(request)

    @staticmethod
    def has_amzn_oidc_headers(meta):
        """
        Check expected JWT AMZN_OIDC_* headers are in request.META

        :param meta:
        :return:
        """
        return aws.AMZN_OIDC_ACCESS_TOKEN in meta and aws.AMZN_OIDC_IDENTITY in meta and aws.AMZN_OIDC_DATA in meta

    @staticmethod
    def verify_amzn_jwt_structure(encoded_jwt_data):
        """
        Check that AWS JWT structure has 3 sections: header, payload, signature

        :param encoded_jwt_data:
        :return:
        """
        return len(encoded_jwt_data.split(".")) == aws.AWS_JWT_SECTIONS

    def get_public_key(self, encoded_jwt_data):
        """
        Retrieve public key for this JWT using its kid. Additionally store in local cache to avoid re-download.

        :return:
        """
        kid = jwt.get_unverified_headers(encoded_jwt_data).get("kid")

        if kid is None:
            raise ValueError("JWT headers must contain kid field", encoded_jwt_data)

        if kid in self.cache_holder:
            return self.cache_holder.get(kid)

        resp = requests.get(aws.AWS_ELB_PUBLIC_KEY_ENDPOINT + kid)
        public_key = resp.text
        self.cache_holder[kid] = public_key

        return public_key

    @staticmethod
    def get_verified_jwt_claims(encoded_jwt_data, public_key):
        """
        Audit JWT token: verify signature, issuer, expire, etc and return verified payload claims

        :param encoded_jwt_data:
        :param public_key:
        :return:
        """
        try:
            return jwt.decode(encoded_jwt_data, public_key, algorithms=[aws.AWS_JWT_SIGNATURE_ALGORITHM])
        except Exception as e:
            raise

    @staticmethod
    def get_alb_session_cookies(http_cookie):
        """
        We parse to SimpleCookie so that we set any http cookie (Morsel object) properties properly if needs be.
        See unit test case.

        :param http_cookie:
        :return:
        """
        cookie = SimpleCookie()
        cookie.load(http_cookie)
        ks = []
        for k in cookie:
            if k.startswith(AWS_ALB_SESSION_COOKIE_PREFIX):
                ks.append(k)
        return ks

    def logout_cognito_user(self, request, response):
        """
        When an application needs to log out an authenticated user, it should set the expiration time of the
        authentication session cookie to -1. And redirect the client to the IdP logout endpoint.

        :param response:
        :param request:
        :return:
        """
        if request.user is not None and request.user.is_authenticated:
            return response

        http_cookie = request.META.get("HTTP_COOKIE")

        if http_cookie is None:
            return response

        alb_session_cookies = self.get_alb_session_cookies(http_cookie)

        if alb_session_cookies:
            resp = HttpResponseRedirect(aws.AWS_COGNITO_IDP_LOGOUT_ENDPOINT)
            for k in alb_session_cookies:
                resp.set_cookie(k, max_age=-1)
            return resp

        return response
