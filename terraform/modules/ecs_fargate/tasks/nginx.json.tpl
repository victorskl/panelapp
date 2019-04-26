[
  {
    "name": "collectstatic",
    "image": "${image}",
    "command": ["python", "/app/panelapp/manage.py", "collectstatic", "--noinput"],
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
      }
    ],
    "mountPoints": [
      {
        "sourceVolume": "static-storage",
        "containerPath": "/static"
      },
      {
        "sourceVolume": "media-storage",
        "containerPath": "/media"
      }
    ],
    "essential": false
  },
  {
    "name": "${container_name}",
    "image": "nginx:1.15.1",
    "cpu": ${cpu},
    "memory": ${memory},
    "networkMode": "${network_mode}",
    "portMappings": [
      {
        "containerPort": 80,
        "protocol": "tcp"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "${log_group}",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "stdout"
      }
    },
    "mountPoints": [
      {
        "sourceVolume": "static-storage",
        "containerPath": "/usr/share/nginx/html/static",
        "readOnly": true
      },
      {
        "sourceVolume": "media-storage",
        "containerPath": "/usr/share/nginx/html/media"
      }
    ],
    "essential": true
  }
]
