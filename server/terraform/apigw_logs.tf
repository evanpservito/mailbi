data "aws_iam_policy_document" "apigw_logs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["apigateway.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "apigw_cloudwatch_role" {
  name               = "${local.project_name}-apigw-cw-role"
  assume_role_policy = data.aws_iam_policy_document.apigw_logs_assume.json
}

data "aws_iam_policy_document" "apigw_logs_policy" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents",
      "logs:GetLogEvents",
      "logs:FilterLogEvents"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "apigw_logs" {
  name   = "${local.project_name}-apigw-logs"
  role   = aws_iam_role.apigw_cloudwatch_role.id
  policy = data.aws_iam_policy_document.apigw_logs_policy.json
}

resource "aws_api_gateway_account" "account" {
  cloudwatch_role_arn = aws_iam_role.apigw_cloudwatch_role.arn
}


