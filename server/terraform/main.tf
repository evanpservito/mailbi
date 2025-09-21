terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  project_name = var.project_name
  lambda_dir   = abspath("${path.module}/../python/lambdas")
}

# IAM role for all Lambda functions
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "${local.project_name}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "lambda_basic_logs" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "lambda_basic_logs" {
  name   = "${local.project_name}-lambda-basic-logs"
  policy = data.aws_iam_policy_document.lambda_basic_logs.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_basic_logs.arn
}

# REQUIRED for Lambda functions configured with VPC access
resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# Optional extra policy for VPC or DB access can be attached externally via var.extra_policy_arns
resource "aws_iam_role_policy_attachment" "extra" {
  count      = length(var.extra_policy_arns)
  role       = aws_iam_role.lambda_role.name
  policy_arn = var.extra_policy_arns[count.index]
}

resource "aws_security_group" "lambda_sg" {
  count       = var.vpc_id != null && (var.vpc_security_group_ids == null || length(var.vpc_security_group_ids) == 0) ? 1 : 0
  name        = "${local.project_name}-lambda-sg"
  description = "Default Lambda security group"
  vpc_id      = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Allow Lambda SG to reach DB SG on db_port, if provided
resource "aws_security_group_rule" "lambda_to_db" {
  count = var.db_security_group_id != null && (
    (var.vpc_security_group_ids != null && length(var.vpc_security_group_ids) > 0) ||
    (var.vpc_id != null && (var.vpc_security_group_ids == null || length(var.vpc_security_group_ids) == 0))
  ) ? 1 : 0
  type                     = "ingress"
  from_port                = var.db_port
  to_port                  = var.db_port
  protocol                 = "tcp"
  source_security_group_id = coalesce(
    try(aws_security_group.lambda_sg[0].id, null),
    try(var.vpc_security_group_ids[0], null)
  )
  security_group_id        = var.db_security_group_id
  description              = "Allow Lambda to DB"
}


