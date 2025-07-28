import pandas as pd
from zenml import step # Changed import
from typing import Annotated

@step
def clean_data_step(df: pd.DataFrame) -> Annotated[pd.DataFrame, "cleaned_df"]:
    """
    Drops missing values from the input DataFrame.
    """
    df.dropna(inplace=True)
    return df
