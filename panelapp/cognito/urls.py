from django.urls import path

from .apps import CognitoConfig
from .views import callback_log
from .views import test

urlpatterns = [
    path('test/', test, name='test'),
    path('callback/login/', callback_log, name='callback_login'),
    path('callback/signout/', callback_log, name='callback_signout'),
]

app_name = CognitoConfig.name
