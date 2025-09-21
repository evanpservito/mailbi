locals {
  # Derive HTTP method from lambda name prefix and path from friendly name
  lambda_routes = { for k, f in aws_lambda_function.this : k => {
    base_name = trimprefix(k, "lambda_")
    method    = upper(lookup({ create = "POST", insert = "POST", select = "GET", delete = "DELETE", update = "PUT" }, split(trimprefix(k, "lambda_"), "_")[0], "POST"))
    path_part = replace(trimprefix(k, "lambda_"), "_", "-")
  } }
}

# REST API
resource "aws_api_gateway_rest_api" "api" {
  name = "${local.project_name}-api"
}

# Authorizer
resource "aws_api_gateway_authorizer" "cognito" {
  name          = "${local.project_name}-cognito-authorizer"
  rest_api_id   = aws_api_gateway_rest_api.api.id
  type          = "COGNITO_USER_POOLS"
  identity_source = "method.request.header.Authorization"
  provider_arns = [var.cognito_user_pool_arn]
}

# One resource per Lambda under root
resource "aws_api_gateway_resource" "route" {
  for_each    = local.lambda_routes
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = each.value.path_part
}

# Methods secured by Cognito and API Key
resource "aws_api_gateway_method" "method" {
  for_each           = local.lambda_routes
  rest_api_id        = aws_api_gateway_rest_api.api.id
  resource_id        = aws_api_gateway_resource.route[each.key].id
  http_method        = each.value.method
  authorization      = "COGNITO_USER_POOLS"
  authorizer_id      = aws_api_gateway_authorizer.cognito.id
  api_key_required   = true
}

# Lambda proxy integration
resource "aws_api_gateway_integration" "integration" {
  for_each                = local.lambda_routes
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.route[each.key].id
  http_method             = aws_api_gateway_method.method[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.this[each.key].invoke_arn
}

# Permission for API Gateway to invoke each Lambda
resource "aws_lambda_permission" "apigw" {
  for_each      = aws_lambda_function.this
  statement_id  = "AllowAPIGatewayInvoke-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = each.value.arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

# Deployment & Stage
resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  triggers = {
    redeploy = sha1(jsonencode({
      resources   = [for k, r in aws_api_gateway_resource.route : r.id]
      methods     = [for k, m in aws_api_gateway_method.method : m.id]
      integrations= [for k, i in aws_api_gateway_integration.integration : i.id]
    }))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  stage_name    = var.api_stage_name
  rest_api_id   = aws_api_gateway_rest_api.api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}

# Require API key usage plan and key
resource "aws_api_gateway_api_key" "key" {
  name = "${local.project_name}-api-key"
}

resource "aws_api_gateway_usage_plan" "plan" {
  name = "${local.project_name}-usage-plan"

  api_stages {
    api_id = aws_api_gateway_rest_api.api.id
    stage  = aws_api_gateway_stage.stage.stage_name
  }

  throttle_settings {
    burst_limit = var.usage_burst_limit
    rate_limit  = var.usage_rate_limit
  }
}

resource "aws_api_gateway_usage_plan_key" "key_attachment" {
  key_id        = aws_api_gateway_api_key.key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.plan.id
}


