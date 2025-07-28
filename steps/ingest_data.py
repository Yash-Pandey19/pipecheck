import pandas as pd
from zenml import step # Changed import
# from zenml.steps import Output # No longer needed

@step
def ingest_data_step() -> pd.DataFrame:
    df = pd.read_csv("data/input.csv")
    return df
