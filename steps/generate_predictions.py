import pandas as pd
import numpy as np
from zenml import step
from typing import Annotated

@step
def generate_predictions_step(input_df: pd.DataFrame) -> Annotated[pd.DataFrame, "predicted_df"]:
    """
    Simulates a model prediction and saves the result to evidently_report/output.csv.
    """
    df = input_df.copy()

    # Simulate predictions: here, randomly assign 0 or 1
    df["prediction"] = np.random.choice([0, 1], size=len(df))

    # Save for Evidently comparison
    df.to_csv("evidently_report/output.csv", index=False)

    print("✅ output.csv generated with predictions at evidently_report/output.csv.")

    return df
