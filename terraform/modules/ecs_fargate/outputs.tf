output "dns_name" {
  description = "The DNS name of the load balancer."
  value = "${local.lb_dns_name}"
}

output "panel_app_base_url" {
  description = "App Base URL"
  value = "${local.base_url}"
}
