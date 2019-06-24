[
  {
    "name": "db_migrate",
    "image": "${image}",
    "entrypoint": ["bash", "-c", "python /app/panelapp/manage.py migrate && python /app/panelapp/manage.py createsuperuser2 --username ${admin_username} --email ${admin_email} --password ${admin_password} --preserve --noinput"],
    "memory": ${memory},
    "networkMode": "${network_mode}",
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${log_group}",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "stdout"
      }
    },
    "environment": [
      {
        "name": "AWS_REGION",
        "value": "${region}"
      },
      {
        "name": "DATABASE_URL",
        "value": "${database_url}"
      },
      {
        "name": "DJANGO_SETTINGS_MODULE",
        "value": "${django_settings_module}"
      },
      {
        "name": "DJANGO_LOG_LEVEL",
        "value": "${django_log_level}"
      }
    ],
    "essential": false
  },
  {
    "name": "${container_name}",
    "image": "${image}",
    "entrypoint": ["bash", "-c", "pip install celery[sqs] && /usr/local/bin/gunicorn panelapp.wsgi --chdir=/app/panelapp -w 4 -b 0.0.0.0:8000"],
    "portMappings": [
      {
        "containerPort": 8000
      }
    ],
    "cpu": ${cpu},
    "memory": ${memory},
    "networkMode": "${network_mode}",
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${log_group}",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "stdout"
      }
    },
    "environment": [
      {
        "name": "AWS_REGION",
        "value": "${region}"
      },
      {
        "name": "AWS_COGNITO_DOMAIN_PREFIX",
        "value": "${aws_cognito_domain_prefix}"
      },
      {
        "name": "AWS_COGNITO_USER_POOL_CLIENT_ID",
        "value": "${aws_cognito_user_pool_client_id}"
      },
      {
        "name": "DATABASE_URL",
        "value": "${database_url}"
      },
      {
        "name": "DJANGO_SETTINGS_MODULE",
        "value": "${django_settings_module}"
      },
      {
        "name": "DJANGO_LOG_LEVEL",
        "value": "${django_log_level}"
      },
      {
        "name": "STATIC_ROOT",
        "value": "${static_root}"
      },
      {
        "name": "MEDIA_ROOT",
        "value": "${media_root}"
      },
      {
        "name": "CELERY_BROKER_URL",
        "value": "${celery_broker_url}"
      },
      {
        "name": "HEALTH_ACCESS_TOKEN_LOCATION",
        "value": "${health_access_token_location}"
      },
      {
        "name": "ALLOWED_HOSTS",
        "value": "${allowed_hosts}"
      },
      {
        "name": "SECRET_KEY",
        "value": "${django_secret_key}"
      },
      {
        "name": "DEBUG",
        "value": "False"
      },
      {
        "name": "DJANGO_ADMIN_URL",
        "value": "${django_admin_url}"
      },
      {
        "name": "EMAIL_HOST",
        "value": "${email_host}"
      },
      {
        "name": "EMAIL_HOST_USER",
        "value": "${email_host_user}"
      },
      {
        "name": "EMAIL_HOST_PASSWORD",
        "value": "${email_host_password}"
      },
      {
        "name": "EMAIL_PORT",
        "value": "${email_port}"
      },
      {
        "name": "EMAIL_USE_TLS",
        "value": "${email_use_tls}"
      },
      {
        "name": "DEFAULT_FROM_EMAIL",
        "value": "${default_from_email}"
      },
      {
        "name": "PANEL_APP_EMAIL",
        "value": "${panel_app_email}"
      },
      {
        "name": "PANEL_APP_BASE_URL",
        "value": "${panel_app_base_url}"
      }
    ],
    "essential": true
  }
]
