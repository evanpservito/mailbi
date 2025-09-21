variable "create_python_layer" {
  description = "Create a Lambda layer from server/requirements.txt"
  type        = bool
  default     = true
}

# (not used in Terraform; build occurs outside with Docker)
# variable "requirements_file" {
#   description = "Path to requirements.txt"
#   type        = string
# }

locals {
  layer_zip_path = "${path.root}/../lambda_layer.zip"
}

# Layer from prebuilt zip at ../lambda_layer.zip
resource "aws_lambda_layer_version" "deps" {
  count               = var.create_python_layer ? 1 : 0
  layer_name          = "${local.project_name}-python-deps"
  description         = "Python dependencies layer"
  filename            = local.layer_zip_path
  compatible_runtimes = ["python3.12"]
}


