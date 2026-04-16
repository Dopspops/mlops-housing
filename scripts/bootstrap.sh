#!/bin/bash
set -e

BUCKET="mlops-housing-artifacts"
APP_DIR="/home/ec2-user/app"

yum update -y
yum install -y python3-pip git

mkdir -p "$APP_DIR"
cd "$APP_DIR"

pip3 install scikit-learn joblib boto3 fastapi uvicorn pydantic

# Download source files uploaded by CI pipeline
aws s3 cp "s3://$BUCKET/src/train.py" train.py
aws s3 cp "s3://$BUCKET/src/app.py" app.py

# Run training — saves model locally and uploads to S3
python3 train.py

# Start FastAPI server
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > /home/ec2-user/server.log 2>&1 &
