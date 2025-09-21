locals {
  # List of python files under lambdas directory
  lambda_files = tolist(fileset(local.lambda_dir, "*.py"))

  # Derive function logical names and resource-friendly names
  lambda_defs = [for f in local.lambda_files : {
    file_name         = f
    base_name         = trimsuffix(f, ".py")
    function_name     = replace(trimsuffix(f, ".py"), "_", "-")
    handler_module    = trimsuffix(f, ".py")
    handler_entry     = "lambda_handler"
    archive_basename  = replace(trimsuffix(f, ".py"), "_", "-")
  }]

  # Friendly names without the leading "lambda_" and with dashes
  lambda_friendly_name = { for d in local.lambda_defs : d.base_name => replace(trimprefix(d.base_name, "lambda_"), "_", "-") }
}

# Package each lambda script into a zip
resource "archive_file" "lambda_zip" {
  for_each    = { for d in local.lambda_defs : d.base_name => d }
  type        = "zip"
  source_file = abspath("${local.lambda_dir}/${each.value.file_name}")
  output_path = abspath("${path.module}/build/${each.value.archive_basename}.zip")
}

# Create one Lambda function per script
resource "aws_lambda_function" "this" {
  for_each         = archive_file.lambda_zip
  function_name    = "${local.project_name}-${local.lambda_friendly_name[each.key]}"
  filename         = each.value.output_path
  source_code_hash = each.value.output_base64sha256
  role             = aws_iam_role.lambda_role.arn
  handler          = "${each.key}.lambda_handler"
  runtime          = "python3.12"
  timeout          = var.lambda_timeout
  memory_size      = var.lambda_memory
  layers           = concat(var.lambda_layer_arns, try([aws_lambda_layer_version.deps[0].arn], []))

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

# Ensure a log group exists per function with retention
resource "aws_cloudwatch_log_group" "lambda" {
  for_each          = aws_lambda_function.this
  name              = "/aws/lambda/${each.value.function_name}"
  retention_in_days = var.log_retention_days
}


