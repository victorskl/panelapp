[
  {
    "name": "db_migrate",
    "image": "${image}",
    "command": ["python", "/app/panelapp/manage.py", "migrate"],
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
      }
    ],
    "essential": false
  },
  {
    "name": "${container_name}",
    "image": "${image}",
    "command": ["/usr/local/bin/gunicorn", "panelapp.wsgi", "--chdir=/app/panelapp", "-w", "4", "-b", "0.0.0.0:8000"],
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
        "value": "/app/health_token"
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
      }
    ],
    "essential": true
  }
]
