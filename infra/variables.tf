variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "key_pair_name" {
  description = "Name of the SSH key pair for EC2 access"
  type        = string
  default     = "MLOps_Access"
}

variable "bucket_name" {
  description = "S3 bucket for data and model artifacts"
  type        = string
  default     = "mlops-housing-artifacts-2026"
}
