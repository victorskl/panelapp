terraform {
  required_version = "~> 0.11.6"

  backend "s3" {}
}

locals {
  envs = {
    default = "dev"
    prod = "prod"
    stag = "staging"
  }

  env = "${lookup(local.envs, terraform.workspace)}"
}

provider "random" {
  version = "~> 2.1"
}

provider "template" {
  version = "~> 2.1"
}

provider "aws" {
  version = "~> 2.5"
  region = "${var.region}"
}


//--- Parameter Store

data "aws_ssm_parameter" "db_password" {
  name = "/panelapp/${local.env}/database/master_password"
}

data "aws_ssm_parameter" "db_username" {
  name = "/panelapp/${local.env}/database/master_username"
}

data "aws_ssm_parameter" "db_name" {
  name = "/panelapp/${local.env}/database/db_name"
}

data "aws_ssm_parameter" "django_secret_key" {
  name = "/panelapp/${local.env}/django/secret_key"
}

data "aws_ssm_parameter" "email_host" {
  name = "/panelapp/${local.env}/email/host"
}

data "aws_ssm_parameter" "email_host_user" {
  name = "/panelapp/${local.env}/email/user"
}

data "aws_ssm_parameter" "email_host_password" {
  name = "/panelapp/${local.env}/email/password"
}


//--- Use default VPC

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "all" {
  vpc_id = "${data.aws_vpc.default.id}"
}

resource "random_string" "admin_password" {
  length = 16
  special = false
}

//--- RDS

resource "aws_security_group" "rds_sg" {
  name = "${var.app_name}-${local.env}-rds-sg"
  description = "RDS Trusted Security Group created by ${var.app_name}-${local.env}"
  vpc_id = "${data.aws_vpc.default.id}"

  ingress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    self = true
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "db" {
  source = "terraform-aws-modules/rds/aws"
  version = "1.28.0"

  identifier = "${data.aws_ssm_parameter.db_name.value}db${local.env}"
  name = "${data.aws_ssm_parameter.db_name.value}db${local.env}"
  username = "${data.aws_ssm_parameter.db_username.value}"
  password = "${data.aws_ssm_parameter.db_password.value}"

  instance_class = "${var.db_instance_class}"
  allocated_storage = "${var.db_allocated_storage}"

  port = "5432"
  engine = "postgres"
  engine_version = "9.6.11"
  major_engine_version = "9.6"
  family = "postgres9.6"

  subnet_ids = ["${data.aws_subnet_ids.all.ids}"]
  vpc_security_group_ids = ["${aws_security_group.rds_sg.id}"]

  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window = "03:00-06:00"
  backup_retention_period = 0

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
}


//--- ECS Fargate

module "ecs" {
  source = "../../modules/ecs_fargate"

  environment = "${local.env}"
  region = "${var.region}"
  vpc_id = "${data.aws_vpc.default.id}"
  subnets_ids = "${data.aws_subnet_ids.all.ids}"
  security_groups_ids = ["${aws_security_group.rds_sg.id}"]

  image = "${var.image}"
  database_url = "postgres://${module.db.this_db_instance_username}:${data.aws_ssm_parameter.db_password.value}@${module.db.this_db_instance_endpoint}/${module.db.this_db_instance_name}"
  django_secret_key = "${data.aws_ssm_parameter.django_secret_key.value}"
  django_admin_url = "${var.django_admin_url}"
  django_settings_module = "${var.django_settings_module}"
  health_access_token_location = "${var.health_access_token_location}"

  celery_broker_url = "sqs://"

  // email settings

  email_host = "${data.aws_ssm_parameter.email_host.value}"
  email_host_user = "${data.aws_ssm_parameter.email_host_user.value}"
  email_host_password = "${data.aws_ssm_parameter.email_host_password.value}"
  email_port = "${var.email_port}"
  email_use_tls = "${var.email_use_tls}"

  default_from_email = "${var.default_from_email}"
  panel_app_email = "${var.panel_app_email}"

  app_domain_name = "${var.app_domain_name}"
  app_domain_parent = "${var.app_domain_parent}"

  // optional variables

  app_name = "${var.app_name}"

  nginx_cpu = "${var.nginx_cpu}"
  nginx_memory = "${var.nginx_memory}"
  nginx_replica = "${var.nginx_replica}"
  nginx_container_name = "${var.nginx_container_name}"

  app_cpu = "${var.app_cpu}"
  app_memory = "${var.app_memory}"
  app_replica = "${var.app_replica}"
  app_container_name = "${var.app_container_name}"

  worker_cpu = "${var.worker_cpu}"
  worker_memory = "${var.worker_memory}"
  worker_replica = "${var.worker_replica}"
  worker_container_name = "${var.worker_container_name}"

  admin_username = "${var.admin_username}"
  admin_email = "${var.admin_email}"
  admin_password = "${random_string.admin_password.result}"

  create_cert = "${var.create_cert}"
  use_cognito = "${var.use_cognito}"
}
