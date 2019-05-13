[
  {
    "name": "${container_name}",
    "image": "${image}",
    "entrypoint": ["bash", "-c", "pip install celery[sqs] && celery worker -A panelapp --workdir /app/panelapp -E -l info"],
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
        "name": "CELERY_BROKER_URL",
        "value": "${celery_broker_url}"
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
