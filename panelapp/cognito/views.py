from datetime import datetime
from pprint import pformat

import boto3
from django.shortcuts import HttpResponse
from django.shortcuts import render

AWS_KEY = None
AWS_SECRET = None
AWS_REGION = None
USER_POOL_ID = None
USER_POOL_ARN = None
APP_CLIENT_ID = None
APP_CLIENT_SECRET = None


def test(request):
    print('>' * 100)
    print('TIME:     %s' % datetime.now())
    print('PATH:     %s' % request.path)
    if request.method == 'GET':
        print('GET:      %s' % str(request.GET))
    elif request.method == 'POST':
        print('POST:     %s' % str(request.POST))
    else:
        print('METHOD:   %s' % request.method)
    print('COOKIES:  %s' % str(request.COOKIES))
    print('<' * 100)

    token = request.META.get('HTTP_X_AMZN_OIDC_ACCESSTOKEN')
    aws_user = None
    error = None
    if AWS_KEY and token:
        try:
            client = boto3.client(
                service_name='cognito-idp',
                region_name=AWS_REGION,
                aws_access_key_id=AWS_KEY,
                aws_secret_access_key=AWS_SECRET,
            )
            aws_user = pformat(client.get_user(AccessToken=token))
        except Exception as e:
            error = str(e)

    headers = sorted(request.META.items(), key=lambda pair: pair[0])
    return render(request, 'cognito/test.html', {
        'headers': headers,
        'error': error,
        'aws_user': aws_user
    })


def callback_log(request):
    print('>' * 100)
    print('TIME:     %s' % datetime.now())
    print('PATH:     %s' % request.path)
    if request.method == 'GET':
        print('GET:      %s' % str(request.GET))
    elif request.method == 'POST':
        print('POST:     %s' % str(request.POST))
    else:
        print('METHOD:   %s' % request.method)
    print('COOKIES:  %s' % str(request.COOKIES))
    print('<' * 100)
    return HttpResponse()
