from .base import *  # noqa

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

AWS_ALB_SESSION_COOKIE_PREFIX = os.getenv("AWS_ALB_SESSION_COOKIE_PREFIX", "AWSELBAuthSessionCookie")

AWS_ELB_PUBLIC_KEY_ENDPOINT = "https://public-keys.auth.elb.{}.amazonaws.com/".format(AWS_REGION)

AWS_COGNITO_DOMAIN_PREFIX = os.getenv("AWS_COGNITO_DOMAIN_PREFIX", "")
AWS_COGNITO_USER_POOL_CLIENT_ID = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID", "")

AWS_COGNITO_HOSTED_AUTH_BASE = "https://{}.auth.{}.amazoncognito.com/".format(AWS_COGNITO_DOMAIN_PREFIX, AWS_REGION)

AWS_COGNITO_IDP_LOGOUT_ENDPOINT = AWS_COGNITO_HOSTED_AUTH_BASE \
        + "logout?&client_id={}&logout_uri={}&redirect_uri={}&response_type=code" \
        .format(AWS_COGNITO_USER_POOL_CLIENT_ID, PANEL_APP_BASE_URL+"/accounts/logout/", PANEL_APP_BASE_URL)

AWS_JWT_SECTIONS = os.getenv("AWS_JWT_SECTIONS", 3)
AWS_JWT_SIGNATURE_ALGORITHM = os.getenv("AWS_JWT_SIGNATURE_ALGORITHM", "ES256")

AMZN_OIDC_ACCESS_TOKEN = os.getenv("AMZN_OIDC_ACCESS_TOKEN", "HTTP_X_AMZN_OIDC_ACCESSTOKEN")
AMZN_OIDC_IDENTITY = os.getenv("AMZN_OIDC_IDENTITY", "HTTP_X_AMZN_OIDC_IDENTITY")
AMZN_OIDC_DATA = os.getenv("AMZN_OIDC_DATA", "HTTP_X_AMZN_OIDC_DATA")

LOGOUT_REDIRECT_URL = os.getenv("LOGOUT_REDIRECT_URL", "home")  # redirect home to break login loop

INSTALLED_APPS += ("cognito",)  # noqa

MIDDLEWARE += ("cognito.middleware.ALBAuthMiddleware",)  # noqa

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.RemoteUserBackend",
    "django.contrib.auth.backends.ModelBackend",
]

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "sqs://")
CELERY_TASK_DEFAULT_QUEUE = os.getenv("CELERY_TASK_DEFAULT_QUEUE", "celery")
