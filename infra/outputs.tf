output "ec2_public_ip" {
  description = "Public IP of the MLOps EC2 instance"
  value       = aws_instance.mlops.public_ip
}

output "s3_bucket_name" {
  description = "Name of the S3 artifacts bucket"
  value       = aws_s3_bucket.artifacts.bucket
}
