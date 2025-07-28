# steps/evaluate_model.py

from zenml import step # Changed import
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from typing import Any

@step
def evaluate_model_step(df: pd.DataFrame, model: Any) -> None:
    X = df.drop("target", axis=1)
    y = df["target"]
    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)
    print(f"✅ Model Accuracy: {accuracy}")
