from fastapi.testclient import TestClient
import numpy as np

from src.app import app


client = TestClient(app)


class MockModel:
    def predict(self, X):
        return np.array([123.45])


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert "model_loaded" in data


def test_predict_success(monkeypatch):
    from src import app as app_module
    app_module.model = MockModel()

    payload = {
        "features": [1.0] * 8
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "prediction" in data
    assert isinstance(data["prediction"], float)


def test_predict_model_not_loaded(monkeypatch):
    from src import app as app_module
    app_module.model = None

    payload = {
        "features": [1.0] * 8
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 503


def test_predict_invalid_input():
    payload = {
        "features": [1.0, 2.0]
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422