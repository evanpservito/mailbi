locals {
  archive_src_dir  = abspath("${path.module}/../archive")
  archive_zip_path = abspath("${path.module}/../archive/build/mailbi-archive.zip")
  pgboto3_layer_zip = abspath("${path.module}/../archive/layers/pgboto3.zip")
}

# IAM for archive lambda
data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "archive_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "archive_role" {
  name               = "${local.project_name}-archive-role"
  assume_role_policy = data.aws_iam_policy_document.archive_assume.json
}

# Secrets Manager access
data "aws_iam_policy_document" "archive_secrets" {
  statement {
    sid     = "SecretsManagerRead"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret"
    ]
    resources = [
      "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:*"
    ]
  }
}

resource "aws_iam_policy" "archive_secrets" {
  name   = "${local.project_name}-archive-secrets"
  policy = data.aws_iam_policy_document.archive_secrets.json
}

# Optional S3 access for specified buckets
data "aws_iam_policy_document" "archive_s3" {
  count = length(var.archive_s3_bucket_arns) > 0 ? 1 : 0
  statement {
    sid     = "S3ReadWrite"
    actions = [
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject",
      "s3:AbortMultipartUpload",
      "s3:ListBucketMultipartUploads"
    ]
    resources = concat(
      var.archive_s3_bucket_arns,
      [for b in var.archive_s3_bucket_arns : "${b}/*"]
    )
  }
}

resource "aws_iam_policy" "archive_s3" {
  count  = length(var.archive_s3_bucket_arns) > 0 ? 1 : 0
  name   = "${local.project_name}-archive-s3"
  policy = data.aws_iam_policy_document.archive_s3[0].json
}

resource "aws_iam_role_policy_attachment" "archive_basic_logs" {
  role       = aws_iam_role.archive_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "archive_vpc_access" {
  role       = aws_iam_role.archive_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy_attachment" "archive_secrets_attach" {
  role       = aws_iam_role.archive_role.name
  policy_arn = aws_iam_policy.archive_secrets.arn
}

resource "aws_iam_role_policy_attachment" "archive_s3_attach" {
  count      = length(var.archive_s3_bucket_arns) > 0 ? 1 : 0
  role       = aws_iam_role.archive_role.name
  policy_arn = aws_iam_policy.archive_s3[0].arn
}

# Zip the archive handler code
resource "archive_file" "mailbi_archive_zip" {
  type        = "zip"
  source_file = "${local.archive_src_dir}/handler.py"
  output_path = local.archive_zip_path
}

# External layer for archive function (prebuilt outside Terraform)
resource "aws_lambda_layer_version" "archive_pgboto3" {
  layer_name          = "${local.project_name}-archive-pg"
  description         = "psycopg2-binary"
  filename            = local.pgboto3_layer_zip
  compatible_runtimes = ["python3.12"]
}

resource "aws_lambda_function" "mailbi_archive" {
  function_name    = "mailbi-archive"
  filename         = archive_file.mailbi_archive_zip.output_path
  source_code_hash = archive_file.mailbi_archive_zip.output_base64sha256
  role             = aws_iam_role.archive_role.arn
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory
  layers           = compact(concat(
    var.lambda_layer_arns,
    [aws_lambda_layer_version.archive_pgboto3.arn]
  ))

  environment {
    variables = var.lambda_environment
  }

  dynamic "vpc_config" {    
    for_each = var.vpc_subnet_ids != null && length(var.vpc_subnet_ids) > 0 ? [1] : []
    content {
      subnet_ids         = var.vpc_subnet_ids
      security_group_ids = var.vpc_security_group_ids != null && length(var.vpc_security_group_ids) > 0 ? var.vpc_security_group_ids : (aws_security_group.lambda_sg[*].id)
    }
  }
}

resource "aws_cloudwatch_log_group" "mailbi_archive" {
  name              = "/aws/lambda/${aws_lambda_function.mailbi_archive.function_name}"
  retention_in_days = var.log_retention_days
}


