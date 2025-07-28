from zenml import step # Changed import
# from zenml.steps import Output # No longer needed
import pandas as pd
from sklearn.linear_model import LogisticRegression
from typing import Any # Added for compatibility if LogisticRegression isn't explicitly imported everywhere it's used as a type hint

@step
def train_model_step(df: pd.DataFrame) -> Any: # Changed return type to Any for broader compatibility if LogisticRegression not directly imported in pipeline
    X = df.drop("target", axis=1)
    y = df["target"]
    model = LogisticRegression()
    model.fit(X, y)
    return model
