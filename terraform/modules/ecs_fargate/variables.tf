variable "app_name" {
  description = "Applicaiton name"
  default = "panelapp"
}

variable "environment" {
  description = "Deployment environment"
}

variable "region" {
  description = "AWS Region"
}

variable "vpc_id" {
  description = "AWS VPC ID"
}

variable "subnets_ids" {
  description = "Default subnets IDs"
  type = "list"
}

variable "security_groups_ids" {
  description = "List of security groups to use with ECS"
  type        = "list"
}

variable "network_mode" {
  description = "Values are none, bridge, awsvpc, and host"
  default = "awsvpc"
}

variable "nginx_cpu" {
  description = "CPU for running Nginx staticfile serving"
  default = "1024"
}

variable "nginx_memory" {
  description = "Memory for running Nginx staticfile serving"
  default = "2048"
}

variable "nginx_replica" {
  description = "Number of Nginx replica count"
  default = 1
}

variable "nginx_container_name" {
  default = "nginx"
}

variable "app_cpu" {
  description = "CPU for running Django PanelApp"
  default = "2048"
}

variable "app_memory" {
  description = "Memory for running Django PanelApp"
  default = "8192"
}

variable "app_replica" {
  description = "Number of Django PanelApp replica count"
  default = 1
}

variable "app_container_name" {
  default = "web"
}

variable "image" {
  description = "PanelApp Docker Image Registry URL"
}

variable "database_url" {
  description = "PanelApp DB Connection String"
}

variable "django_settings_module" {
  description = "e.g. DJANGO_SETTINGS_MODULE=panelapp.settings.dev"
  default = "panelapp.settings.production"
}

variable "django_log_level" {
  description = "e.g. DJANGO_LOG_LEVEL=INFO"
  default = "INFO"
}

variable "django_secret_key" {
  description = "Django SECRET_KEY"
}

variable "static_root" {
  description = "Django STATIC_ROOT"
  default = "/static"
}

variable "media_root" {
  description = "Django MEDIA_ROOT"
  default = "/media"
}

variable "allowed_hosts" {
  description = "Django ALLOWED_HOSTS"
  default = "*"
}

variable "celery_broker_url" {
  description = "celery_broker_url"
  default = "amqp://rabbitmq/panelapp"
}
