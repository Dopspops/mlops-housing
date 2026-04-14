terraform {
  backend "s3" {
    bucket         = "mlops-housing-tfstate"
    key            = "state/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "tfstate-lock"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}