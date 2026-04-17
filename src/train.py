import joblib
import boto3
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

BUCKET_NAME = "mlops-housing-artifacts"
MODEL_S3_KEY = "models/model.joblib"
MODEL_LOCAL_PATH = "/home/ec2-user/model.joblib"


def load_data():
    data = fetch_california_housing()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def save_model(model):
    joblib.dump(model, MODEL_LOCAL_PATH)


def upload_model():
    s3 = boto3.client("s3")
    s3.upload_file(MODEL_LOCAL_PATH, BUCKET_NAME, MODEL_S3_KEY)
    print(f"Modelo subido a s3://{BUCKET_NAME}/{MODEL_S3_KEY}")


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = load_data()
    model = train_model(X_train, y_train)
    save_model(model)
    upload_model()
    print("Entrenamiento completado.")
