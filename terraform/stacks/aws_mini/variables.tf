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
