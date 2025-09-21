variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix for resource names"
  type        = string
  default     = "mailbi"
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}

variable "lambda_memory" {
  description = "Lambda memory size in MB"
  type        = number
  default     = 256
}

variable "lambda_environment" {
  description = "Environment variables for Lambda functions"
  type        = map(string)
  default     = {}
}

variable "lambda_layer_arns" {
  description = "Optional list of layer ARNs to attach to functions"
  type        = list(string)
  default     = []
}

variable "vpc_subnet_ids" {
  description = "Optional VPC subnet IDs for Lambda"
  type        = list(string)
  default     = null
}

variable "vpc_security_group_ids" {
  description = "Optional VPC security group IDs for Lambda"
  type        = list(string)
  default     = null
}

variable "vpc_id" {
  description = "VPC ID used to optionally create a Lambda security group when vpc_security_group_ids is not provided"
  type        = string
  default     = null
}

variable "extra_policy_arns" {
  description = "Optional extra IAM policy ARNs to attach to the Lambda role"
  type        = list(string)
  default     = []
}

variable "log_retention_days" {
  description = "CloudWatch Logs retention in days"
  type        = number
  default     = 14
}

variable "api_stage_name" {
  description = "API Gateway stage name"
  type        = string
  default     = "prod"
}

variable "usage_burst_limit" {
  description = "Usage plan burst limit"
  type        = number
  default     = 50
}

variable "usage_rate_limit" {
  description = "Usage plan rate limit"
  type        = number
  default     = 25
}

variable "cognito_user_pool_arn" {
  description = "Cognito User Pool ARN used for API Gateway authorizer"
  type        = string
  default     = null
}

variable "db_security_group_id" {
  description = "DB security group ID to allow ingress from Lambda"
  type        = string
  default     = null
}

variable "db_port" {
  description = "DB port for ingress rule"
  type        = number
  default     = 5432
}


