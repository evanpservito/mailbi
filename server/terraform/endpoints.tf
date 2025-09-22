locals {
  # Try to determine the Lambda security group to allow as source for VPC endpoints
  lambda_source_sg_id = coalesce(
    try(aws_security_group.lambda_sg[0].id, null),
    try(var.vpc_security_group_ids[0], null)
  )
}

# Security Group for Secrets Manager Interface VPC Endpoint
resource "aws_security_group" "vpce_secrets" {
  count       = var.vpc_id != null && local.lambda_source_sg_id != null ? 1 : 0
  name_prefix = "${local.project_name}-secrets-vpce"
  description = "Allow Lambda SG to reach Secrets Manager VPC endpoint"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [local.lambda_source_sg_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Secrets Manager Interface Endpoint
resource "aws_vpc_endpoint" "secretsmanager" {
  count                = var.vpc_id != null && var.vpc_subnet_ids != null && length(var.vpc_subnet_ids) > 0 ? 1 : 0
  vpc_id               = var.vpc_id
  service_name         = "com.amazonaws.${var.aws_region}.secretsmanager"
  vpc_endpoint_type    = "Interface"
  private_dns_enabled  = true
  subnet_ids           = var.vpc_subnet_ids
  security_group_ids   = aws_security_group.vpce_secrets[*].id
}

# IAM permissions for Lambda to access Secrets Manager
data "aws_iam_policy_document" "lambda_secrets_access" {
  statement {
    sid     = "SecretsRead"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
      "secretsmanager:ListSecretVersionIds"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "lambda_secrets_access" {
  name   = "${local.project_name}-lambda-secrets-access"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.lambda_secrets_access.json
}


