//--- locals

locals {
  lb_dns_name = "${element(concat(aws_lb.main.*.dns_name), 0)}"
  base_url = "https://${var.app_domain_name}"
}


//--- CloudWatch log group

resource "aws_cloudwatch_log_group" "log_group" {
  name = "/ecs/${var.app_name}"
}


//--- IAM Role and Policy

data "aws_iam_policy_document" "ecs_assume_role_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["ecs.amazonaws.com"]
      type = "Service"
    }
  }
}

data "aws_iam_policy_document" "ecs_service_policy" {
  statement {
    effect = "Allow"
    actions = [
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:Describe*",
      "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
      "elasticloadbalancing:DeregisterTargets",
      "elasticloadbalancing:Describe*",
      "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
      "elasticloadbalancing:RegisterTargets"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role" "ecs_service_role" {
  name = "${var.app_name}-${var.environment}-ecsServiceRole"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_assume_role_policy.json}"
}

resource "aws_iam_role_policy" "ecs_service_role_policy" {
  name = "${var.app_name}-${var.environment}-ecsServiceRolePolicy"
  policy = "${data.aws_iam_policy_document.ecs_service_policy.json}"
  role = "${aws_iam_role.ecs_service_role.id}"
}

data "aws_iam_policy_document" "ecs_task_assume_role_policy" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = ["ecs-tasks.amazonaws.com"]
      type = "Service"
    }
  }
}

data "aws_iam_policy_document" "ecs_task_execution_policy" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "sqs:ListQueues",
      "sqs:ChangeMessageVisibility",
      "sqs:ChangeMessageVisibilityBatch",
      "sqs:DeleteMessage",
      "sqs:DeleteMessageBatch",
      "sqs:SendMessage",
      "sqs:SendMessageBatch",
      "sqs:ReceiveMessage",
      "sqs:GetQueueUrl",
      "sqs:GetQueueAttributes",
      "sqs:CreateQueue",
      "sqs:DeleteQueue",
      "sqs:SetQueueAttributes"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.app_name}-${var.environment}-ecsTaskExecutionRole"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_task_assume_role_policy.json}"
}

resource "aws_iam_role_policy" "ecs_task_execution_role_policy" {
  name = "${var.app_name}-${var.environment}-ecsTaskExecutionRolePolicy"
  role = "${aws_iam_role.ecs_task_execution_role.id}"
  policy = "${data.aws_iam_policy_document.ecs_task_execution_policy.json}"
}


//--- ACM and Route53

resource "aws_acm_certificate" "cert" {
  domain_name = "${var.app_domain_name}"
  validation_method = "DNS"
}

resource "aws_acm_certificate_validation" "cert" {
  certificate_arn = "${aws_acm_certificate.cert.arn}"
  validation_record_fqdns = ["${aws_route53_record.cert_validation.fqdn}"]
}

data "aws_route53_zone" "app_dns_zone" {
  name = "${var.app_domain_name}."
  private_zone = false
}

resource "aws_route53_record" "cert_validation" {
  name = "${aws_acm_certificate.cert.domain_validation_options.0.resource_record_name}"
  type = "${aws_acm_certificate.cert.domain_validation_options.0.resource_record_type}"
  zone_id = "${data.aws_route53_zone.app_dns_zone.zone_id}"
  records = ["${aws_acm_certificate.cert.domain_validation_options.0.resource_record_value}"]
  ttl = 60
}

resource "aws_route53_record" "app_dns_record" {
  zone_id = "${data.aws_route53_zone.app_dns_zone.zone_id}"
  name = "${var.app_domain_name}"
  type = "A"

  alias {
    name = "${local.lb_dns_name}"
    zone_id = "${aws_lb.main.zone_id}"
    evaluate_target_health = true
  }
}


//--- ALB

resource "random_id" "target_group_sufix" {
  byte_length = 2
}

resource "aws_lb" "main" {
  name = "${var.app_name}-${var.environment}-alb"
  subnets = ["${var.subnets_ids}"]
  security_groups = ["${aws_security_group.alb_inbound_sg.id}"]
}

resource "aws_lb_listener" "frontend_http" {
  load_balancer_arn = "${aws_lb.main.arn}"
  port = "80"
  protocol = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port = "443"
      protocol = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "frontend" {
  load_balancer_arn = "${aws_lb.main.arn}"
  port = "443"
  protocol = "HTTPS"
  ssl_policy = "ELBSecurityPolicy-2016-08"
  certificate_arn = "${aws_acm_certificate_validation.cert.certificate_arn}"

  default_action {
    type = "forward"
    target_group_arn = "${aws_lb_target_group.app.arn}"
  }

  depends_on = ["aws_lb_target_group.app", "aws_lb_target_group.static"]
}

resource "aws_lb_listener_rule" "static" {
  listener_arn = "${aws_lb_listener.frontend.arn}"
  priority = 100

  action {
    type = "forward"
    target_group_arn = "${aws_lb_target_group.static.arn}"
  }

  condition {
    field = "path-pattern"
    values = ["/static/*"]
  }
}

resource "aws_lb_listener_rule" "media" {
  listener_arn = "${aws_lb_listener.frontend.arn}"
  priority = 101

  action {
    type = "forward"
    target_group_arn = "${aws_lb_target_group.static.arn}"
  }

  condition {
    field = "path-pattern"
    values = ["/media/*"]
  }
}

resource "aws_lb_target_group" "app" {
  name = "${var.app_name}-${var.environment}-app-${random_id.target_group_sufix.hex}"
  port = 8000
  protocol = "HTTP"
  vpc_id = "${var.vpc_id}"
  target_type = "ip"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb_target_group" "static" {
  name = "${var.app_name}-${var.environment}-static-${random_id.target_group_sufix.hex}"
  port = 80
  protocol = "HTTP"
  vpc_id = "${var.vpc_id}"
  target_type = "ip"

  lifecycle {
    create_before_destroy = true
  }
}


//--- Security Group

resource "aws_security_group" "alb_inbound_sg" {
  name = "${var.app_name}-${var.environment}-alb-inbound-sg"
  description = "ELB Allowed Ports created by ${var.app_name}-${var.environment}"
  vpc_id = "${var.vpc_id}"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ecs_service_sg" {
  name = "${var.app_name}-${var.environment}-ecs-service-sg"
  description = "ECS Allowed Ports created by ${var.app_name}-${var.environment}"
  vpc_id = "${var.vpc_id}"

  ingress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    security_groups = ["${aws_security_group.alb_inbound_sg.id}"]
  }

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


//--- ECS

resource "aws_ecs_cluster" "cluster" {
  name = "${var.app_name}-${var.environment}-cluster"
}


// main django app

data "template_file" "web_tpl" {
  template = "${file("${path.module}/tasks/web.json.tpl")}"

  vars {
    region = "${var.region}"
    log_group = "${aws_cloudwatch_log_group.log_group.name}"
    network_mode = "${var.network_mode}"
    cpu = "${var.app_cpu}"
    memory = "${var.app_memory}"

    image = "${var.image}"
    container_name = "${var.app_container_name}"
    database_url = "${var.database_url}"
    django_settings_module = "${var.django_settings_module}"
    django_log_level = "${var.django_log_level}"
    django_secret_key = "${var.django_secret_key}"
    django_admin_url = "${var.django_admin_url}"
    health_access_token_location = "${var.health_access_token_location}"

    static_root = "${var.static_root}"
    media_root = "${var.media_root}"
    allowed_hosts = "${var.allowed_hosts}"
    celery_broker_url = "${var.celery_broker_url}"

    email_host = "${var.email_host}"
    email_host_user = "${var.email_host_user}"
    email_host_password = "${var.email_host_password}"
    email_port = "${var.email_port}"
    email_use_tls = "${var.email_use_tls}"

    default_from_email = "${var.default_from_email}"
    panel_app_email = "${var.panel_app_email}"
    panel_app_base_url = "${local.base_url}"
  }
}

resource "aws_ecs_task_definition" "web" {
  family = "${var.app_name}-${var.environment}-web"
  container_definitions = "${data.template_file.web_tpl.rendered}"
  requires_compatibilities = ["FARGATE"]
  network_mode = "${var.network_mode}"
  cpu = "${var.app_cpu}"
  memory = "${var.app_memory}"
  execution_role_arn = "${aws_iam_role.ecs_task_execution_role.arn}"
  task_role_arn = "${aws_iam_role.ecs_task_execution_role.arn}"
}

resource "aws_ecs_service" "web" {
  name = "${var.app_name}-${var.environment}-web"
  cluster = "${aws_ecs_cluster.cluster.id}"
  task_definition = "${aws_ecs_task_definition.web.arn}"
  desired_count = "${var.app_replica}"
  launch_type = "FARGATE"

  network_configuration {
    subnets = ["${var.subnets_ids}"]
    security_groups = ["${aws_security_group.ecs_service_sg.id}", "${var.security_groups_ids}"]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = "${aws_lb_target_group.app.arn}"
    container_name = "${var.app_container_name}"
    container_port = 8000
  }

  depends_on = ["aws_iam_role_policy.ecs_service_role_policy", "aws_lb_listener.frontend"]
}


// celery worker

data "template_file" "worker_tpl" {
  template = "${file("${path.module}/tasks/worker.json.tpl")}"

  vars {
    region = "${var.region}"
    log_group = "${aws_cloudwatch_log_group.log_group.name}"
    network_mode = "${var.network_mode}"
    cpu = "${var.worker_cpu}"
    memory = "${var.worker_memory}"

    image = "${var.image}"
    container_name = "${var.worker_container_name}"
    database_url = "${var.database_url}"
    django_settings_module = "${var.django_settings_module}"
    django_log_level = "${var.django_log_level}"
    django_secret_key = "${var.django_secret_key}"

    static_root = "${var.static_root}"
    media_root = "${var.media_root}"
    allowed_hosts = "${var.allowed_hosts}"
    celery_broker_url = "${var.celery_broker_url}"

    email_host = "${var.email_host}"
    email_host_user = "${var.email_host_user}"
    email_host_password = "${var.email_host_password}"
    email_port = "${var.email_port}"
    email_use_tls = "${var.email_use_tls}"

    default_from_email = "${var.default_from_email}"
    panel_app_email = "${var.panel_app_email}"
    panel_app_base_url = "${local.base_url}"
  }
}

resource "aws_ecs_task_definition" "worker" {
  family = "${var.app_name}-${var.environment}-worker"
  container_definitions = "${data.template_file.worker_tpl.rendered}"
  requires_compatibilities = ["FARGATE"]
  network_mode = "${var.network_mode}"
  cpu = "${var.worker_cpu}"
  memory = "${var.worker_memory}"
  execution_role_arn = "${aws_iam_role.ecs_task_execution_role.arn}"
  task_role_arn = "${aws_iam_role.ecs_task_execution_role.arn}"
}

resource "aws_ecs_service" "worker" {
  name = "${var.app_name}-${var.environment}-worker"
  cluster = "${aws_ecs_cluster.cluster.id}"
  task_definition = "${aws_ecs_task_definition.worker.arn}"
  desired_count = "${var.worker_replica}"
  launch_type = "FARGATE"

  network_configuration {
    subnets = ["${var.subnets_ids}"]
    security_groups = ["${aws_security_group.ecs_service_sg.id}", "${var.security_groups_ids}"]
    assign_public_ip = true
  }

  depends_on = ["aws_iam_role_policy.ecs_service_role_policy"]
}


// collectstatic and serve through nginx

data "template_file" "static_tpl" {
  template = "${file("${path.module}/tasks/nginx.json.tpl")}"

  vars {
    region = "${var.region}"
    log_group = "${aws_cloudwatch_log_group.log_group.name}"
    network_mode = "${var.network_mode}"
    cpu = "${var.nginx_cpu}"
    memory = "${var.nginx_memory}"

    image = "${var.image}"
    container_name = "${var.nginx_container_name}"
    django_settings_module = "${var.django_settings_module}"
    django_log_level = "${var.django_log_level}"
    static_root = "${var.static_root}"
    media_root = "${var.media_root}"
  }
}

resource "aws_ecs_task_definition" "static" {
  family = "${var.app_name}-${var.environment}-static"
  container_definitions = "${data.template_file.static_tpl.rendered}"
  requires_compatibilities = ["FARGATE"]
  network_mode = "${var.network_mode}"
  cpu = "${var.nginx_cpu}"
  memory = "${var.nginx_memory}"
  execution_role_arn = "${aws_iam_role.ecs_task_execution_role.arn}"
  task_role_arn = "${aws_iam_role.ecs_task_execution_role.arn}"

  volume {
    name = "static-storage"
  }

  volume {
    name = "media-storage"
  }
}

resource "aws_ecs_service" "static" {
  name = "${var.app_name}-${var.environment}-static"
  cluster = "${aws_ecs_cluster.cluster.id}"
  task_definition = "${aws_ecs_task_definition.static.arn}"
  desired_count = "${var.nginx_replica}"
  launch_type = "FARGATE"

  network_configuration {
    subnets = ["${var.subnets_ids}"]
    security_groups = ["${aws_security_group.ecs_service_sg.id}", "${var.security_groups_ids}"]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = "${aws_lb_target_group.static.arn}"
    container_name = "${var.nginx_container_name}"
    container_port = 80
  }

  depends_on = ["aws_iam_role_policy.ecs_service_role_policy", "aws_lb_listener.frontend"]
}
