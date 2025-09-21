output "lambda_function_names" {
  description = "Lambda function names"
  value       = { for k, f in aws_lambda_function.this : k => f.function_name }
}

output "lambda_function_arns" {
  description = "Lambda function ARNs"
  value       = { for k, f in aws_lambda_function.this : k => f.arn }
}

output "lambda_zip_paths" {
  description = "Built zip artifact paths"
  value       = { for k, z in archive_file.lambda_zip : k => z.output_path }
}

output "api_invoke_base_url" {
  description = "Base invoke URL for the API stage"
  value       = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.stage.stage_name}"
}

output "api_key_value" {
  description = "API key value"
  value       = aws_api_gateway_api_key.key.value
  sensitive   = true
}


