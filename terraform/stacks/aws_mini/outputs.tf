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
