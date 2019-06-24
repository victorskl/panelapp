output "workspace" {
  value = "${terraform.workspace}"
}

output "env" {
  value = "${local.env}"
}

output "region" {
  value = "${var.region}"
}

output "vpc_id" {
  value = "${data.aws_vpc.default.id}"
}

output "aws_subnet_ids" {
  value = "${data.aws_subnet_ids.all.ids}"
}

output "dns_name" {
  description = "The DNS name of the load balancer."
  value = "${module.ecs.dns_name}"
}

output "panel_app_base_url" {
  description = "App Base URL"
  value = "${module.ecs.panel_app_base_url}"
}

output "admin_username" {
  description = "Provided admin username."
  value = "${var.admin_username}"
}

output "admin_email" {
  description = "Provided admin email."
  value = "${var.admin_email}"
}

output "admin_password" {
  description = "Randomly generated admin password. Personalise this upon your first login!"
  value = "${random_string.admin_password.result}"
}
