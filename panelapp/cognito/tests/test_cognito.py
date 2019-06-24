import ast
import json
import os

from django.http import SimpleCookie
from django.test import SimpleTestCase
from jose import jwt

from cognito.middleware import ALBAuthMiddleware


class CognitoTestCase(SimpleTestCase):

    def setUp(self) -> None:
        file_path = os.path.join(os.path.dirname(__file__), "fixtures.json")
        test_file = os.path.abspath(file_path)

        with open(test_file) as f:
            mock_data = json.load(f)
            self.mock_encoded_jwt_data = mock_data.get("mock_encoded_jwt_data")
            self.mock_public_key = mock_data.get("mock_public_key")
            self.mock_meta = ast.literal_eval(mock_data.get("mock_meta"))
            self.mock_meta_http_cookie = ast.literal_eval(mock_data.get("mock_meta_http_cookie"))

    def test_has_amzn_oidc_headers(self):
        self.assertTrue(ALBAuthMiddleware.has_amzn_oidc_headers(self.mock_meta))

    def test_confirm_amzn_jwt_structure(self):
        self.assertTrue(ALBAuthMiddleware.verify_amzn_jwt_structure(self.mock_encoded_jwt_data))

    def test_get_verified_jwt_claims(self):
        with self.assertRaisesMessage(Exception, "Signature has expired."):
            claims = ALBAuthMiddleware.get_verified_jwt_claims(self.mock_encoded_jwt_data, self.mock_public_key)
            self.assertIsNone(claims)

    def test_get_alb_session_cookies(self):
        http_cookie = self.mock_meta_http_cookie.get("HTTP_COOKIE")
        self.assertIsNotNone(http_cookie)
        alb_session_cookies = ALBAuthMiddleware.get_alb_session_cookies(http_cookie)
        self.assertTrue(alb_session_cookies)

        cook = SimpleCookie()
        cook.load(http_cookie)
        morsel_keys = cook.get(alb_session_cookies[0]).keys()
        self.assertTrue('expires' in morsel_keys)

    def test_get_public_key(self):
        this = ALBAuthMiddleware(None)
        kid = jwt.get_unverified_headers(self.mock_encoded_jwt_data).get("kid")
        this.cache_holder[kid] = self.mock_public_key
        self.assertEqual(this.get_public_key(self.mock_encoded_jwt_data), self.mock_public_key)
