import numpy as np
from sklearn.linear_model import LinearRegression

MODEL_VERSION = "1.0.0"

_model = LinearRegression()
_model.fit(
    np.array([[1], [2], [3], [4], [5]]),
    np.array([2.1, 4.0, 6.1, 7.9, 10.2]),
)


def predict(features: list[float]) -> float:
    x = np.array(features).reshape(1, -1)
    return float(_model.predict(x)[0])