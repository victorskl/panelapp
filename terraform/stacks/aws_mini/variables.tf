variable "region" {
  description = "Provide AWS Region e.g. ap-southeast-2"
  default = "ap-southeast-2"
}

variable "app_name" {
  default = "panelapp"
}

variable "image" {
  description = "App docker image repo URL"
  default = "victorskl/panelapp"
}

//--- RDS

variable "db_instance_class" {
  description = "Provide db instance class to use e.g. db.t2.micro"
  default = "db.t2.micro"
}

variable "db_allocated_storage" {
  description = "Provide db storage size to use e.g. 10 (for 10GB)"
  default = 5
}

//--- ECS

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

variable "worker_cpu" {
  description = "CPU for running Django PanelApp Celery Worker"
  default = "1024"
}

variable "worker_memory" {
  description = "Memory for running Django PanelApp Celery Worker"
  default = "4096"
}

variable "worker_replica" {
  description = "Number of Django PanelApp Celery Worker replica count"
  default = 1
}

variable "worker_container_name" {
  default = "worker"
}

variable "email_port" {
  description = "Email Port"
  default = 587
}

variable "email_use_tls" {
  description = "Email Use TLS"
  default = "True"
}

variable "default_from_email" {
  description = "PanelApp send emails as this address"
  default = "PanelApp <panelapp@panelapp.local>"
}

variable "panel_app_email" {
  description = "PanelApp email address"
  default = "panelapp@panelapp.local"
}

variable "app_domain_name" {
  description = "App Domain Name"
}

// Optional

variable "health_access_token_location" {
  description = "URL token for authorizing status checks"
  default = "/app/health_token"
}

variable "django_admin_url" {
  description = "To Change Django Admin URL to Something Secure"
  default = "admin/"
}

variable "django_settings_module" {
  description = "e.g. panelapp.settings.production"
  default = "panelapp.settings.aws"
}

variable "admin_username" {
  description = "Admin username (i.e. Django createsuperuser)"
}

variable "admin_email" {
  description = "Admin email address"
}

variable "create_cert" {
  description = "Create a new ACM SSL certificate? (true/false)"
}

variable "use_cognito" {
  description = "Use Cognito? (true/false)"
}
