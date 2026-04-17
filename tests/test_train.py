import os
import tempfile
import joblib

from src import train


def test_load_data():
    X_train, X_test, y_train, y_test = train.load_data()

    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    assert len(y_train) > 0
    assert len(y_test) > 0


def test_train_model():
    X_train, X_test, y_train, y_test = train.load_data()
    model = train.train_model(X_train, y_train)

    assert hasattr(model, "predict")

    sample = X_test[:1]
    prediction = model.predict(sample)

    assert prediction.shape == (1,)


def test_save_model():
    X_train, X_test, y_train, y_test = train.load_data()
    model = train.train_model(X_train, y_train)

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        temp_path = tmp.name

    joblib.dump(model, temp_path)

    assert os.path.exists(temp_path)

    loaded_model = joblib.load(temp_path)
    assert hasattr(loaded_model, "predict")

    os.remove(temp_path)