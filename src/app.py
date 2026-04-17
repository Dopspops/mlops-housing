from __future__ import annotations

from pathlib import Path
from typing import List

import boto3
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

AWS_REGION = "us-east-2"
S3_BUCKET = "mlops-housing-artifacts-2026"
S3_KEY = "models/model.joblib"
LOCAL_MODEL_PATH = "/tmp/model.joblib"
EXPECTED_FEATURES = 8

app = FastAPI(
    title="Housing Inference API",
    version="1.0.0",
    description="FastAPI service for California Housing predictions"
)

model = None


class PredictionRequest(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=EXPECTED_FEATURES,
        max_length=EXPECTED_FEATURES,
        description="Lista de 8 variables numéricas"
    )


class PredictionResponse(BaseModel):
    prediction: float


def download_model_from_s3() -> str:
    s3 = boto3.client("s3", region_name=AWS_REGION)

    local_path = Path(LOCAL_MODEL_PATH)
    local_path.parent.mkdir(parents=True, exist_ok=True)

    s3.download_file(S3_BUCKET, S3_KEY, str(local_path))
    return str(local_path)


def load_model():
    local_model_file = download_model_from_s3()
    return joblib.load(local_model_file)


@app.on_event("startup")
def startup_event():
    global model
    try:
        model = load_model()
        print("Modelo cargado correctamente desde S3")
    except Exception as exc:
        model = None
        print(f"Error cargando modelo desde S3: {exc}")


@app.get("/health")
def health():
    if model is not None:
        return {
            "status": "ok",
            "model_loaded": True,
            "bucket": S3_BUCKET,
            "model_key": S3_KEY,
            "region": AWS_REGION
        }

    return {
        "status": "degraded",
        "model_loaded": False,
        "message": "API is running, but model file was not found in S3.",
        "bucket": S3_BUCKET,
        "model_key": S3_KEY,
        "region": AWS_REGION
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded. The file was not found in S3 yet."
        )

    try:
        features_array = np.array(payload.features, dtype=float).reshape(1, -1)
        prediction = model.predict(features_array)[0]
        return PredictionResponse(prediction=float(prediction))
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Error generating prediction: {str(exc)}"
        ) from exc
