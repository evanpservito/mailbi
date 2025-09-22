locals {
  # Set of existing lambda keys from code
  lambda_keys = toset([for d in local.lambda_defs : d.base_name])

  # Nouns to expose as resources
  nouns = [
    "accounts",
    "customers",
    "mailboxes",
    "messages",
    "packages",
    "stores",
    "user-accounts"
  ]

  # Candidate routes built from nouns/actions
  _candidates = flatten([
    for n in local.nouns : [
      {
        path_part  = n
        method     = "GET"
        lambda_key = "lambda_select_${replace(n, "-", "_" )}"
      },
      {
        path_part  = n
        method     = "POST"
        lambda_key = n == "stores" ? "lambda_create_store_and_admin" : "lambda_insert_${replace(n, "-", "_" )}"
      },
      {
        path_part  = n
        method     = "PUT"
        lambda_key = "lambda_update_${replace(n, "-", "_" )}"
      },
      {
        path_part  = n
        method     = "DELETE"
        lambda_key = "lambda_delete_${replace(n, "-", "_" )}"
      }
    ]
  ])

  # Keep only routes where the target Lambda exists
  _routes = [for r in local._candidates : r if contains(local.lambda_keys, r.lambda_key)]

  resource_names = toset([for r in local._routes : r.path_part])

  # Targets per method keyed by resource path
  get_targets = { for r in local._routes : r.path_part => r.lambda_key if r.method == "GET" }
  post_targets = { for r in local._routes : r.path_part => r.lambda_key if r.method == "POST" }
  put_targets = { for r in local._routes : r.path_part => r.lambda_key if r.method == "PUT" }
  delete_targets = { for r in local._routes : r.path_part => r.lambda_key if r.method == "DELETE" }
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
  for_each    = local.resource_names
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = each.value
}

# Methods secured by Cognito and API Key
resource "aws_api_gateway_method" "get" {
  for_each           = local.get_targets
  rest_api_id        = aws_api_gateway_rest_api.api.id
  resource_id        = aws_api_gateway_resource.route[each.key].id
  http_method        = "GET"
  authorization      = "COGNITO_USER_POOLS"
  authorizer_id      = aws_api_gateway_authorizer.cognito.id
  api_key_required   = true
}

# Lambda proxy integration - GET
resource "aws_api_gateway_integration" "get" {
  for_each                = local.get_targets
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.route[each.key].id
  http_method             = aws_api_gateway_method.get[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.this[each.value].invoke_arn
}

# POST
resource "aws_api_gateway_method" "post" {
  for_each           = local.post_targets
  rest_api_id        = aws_api_gateway_rest_api.api.id
  resource_id        = aws_api_gateway_resource.route[each.key].id
  http_method        = "POST"
  authorization      = "COGNITO_USER_POOLS"
  authorizer_id      = aws_api_gateway_authorizer.cognito.id
  api_key_required   = true
}

resource "aws_api_gateway_integration" "post" {
  for_each                = local.post_targets
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.route[each.key].id
  http_method             = aws_api_gateway_method.post[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.this[each.value].invoke_arn
}

# PUT
resource "aws_api_gateway_method" "put" {
  for_each           = local.put_targets
  rest_api_id        = aws_api_gateway_rest_api.api.id
  resource_id        = aws_api_gateway_resource.route[each.key].id
  http_method        = "PUT"
  authorization      = "COGNITO_USER_POOLS"
  authorizer_id      = aws_api_gateway_authorizer.cognito.id
  api_key_required   = true
}

resource "aws_api_gateway_integration" "put" {
  for_each                = local.put_targets
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.route[each.key].id
  http_method             = aws_api_gateway_method.put[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.this[each.value].invoke_arn
}

# DELETE
resource "aws_api_gateway_method" "delete" {
  for_each           = local.delete_targets
  rest_api_id        = aws_api_gateway_rest_api.api.id
  resource_id        = aws_api_gateway_resource.route[each.key].id
  http_method        = "DELETE"
  authorization      = "COGNITO_USER_POOLS"
  authorizer_id      = aws_api_gateway_authorizer.cognito.id
  api_key_required   = true
}

resource "aws_api_gateway_integration" "delete" {
  for_each                = local.delete_targets
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.route[each.key].id
  http_method             = aws_api_gateway_method.delete[each.key].http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.this[each.value].invoke_arn
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
      methods     = concat(
        [for k, m in aws_api_gateway_method.get : m.id],
        [for k, m in aws_api_gateway_method.post : m.id],
        [for k, m in aws_api_gateway_method.put : m.id],
        [for k, m in aws_api_gateway_method.delete : m.id]
      )
      integrations= concat(
        [for k, i in aws_api_gateway_integration.get : i.id],
        [for k, i in aws_api_gateway_integration.post : i.id],
        [for k, i in aws_api_gateway_integration.put : i.id],
        [for k, i in aws_api_gateway_integration.delete : i.id]
      )
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


