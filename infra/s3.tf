resource "aws_s3_bucket" "artifacts" {
  bucket = var.bucket_name

  tags = {
    Project = "mlops-housing"
  }
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}

