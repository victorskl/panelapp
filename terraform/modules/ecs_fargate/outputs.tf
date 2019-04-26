output "dns_name" {
  description = "The DNS name of the load balancer."
  value = "${element(concat(aws_lb.main.*.dns_name), 0)}"
}
