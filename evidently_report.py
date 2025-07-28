# evidently_report.py

import pandas as pd
from zenml import step
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.pipeline.column_mapping import ColumnMapping

import os

@step
def evidently_report_step(
    reference_data: pd.DataFrame, # This is your cleaned_df (features + target)
    current_data: pd.DataFrame,   # This is your predicted_df (features + target + predictions)
) -> None:
    """
    Generates an Evidently AI data drift report.
    This version explicitly defines features for drift detection and
    handles the 'prediction' column's presence carefully.
    """

    # Ensure the output directory exists
    report_dir = "evidently_report"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "report.html")

    # --- THE CRITICAL CHANGE FOR COLUMN MAPPING ---
    # We need to tell Evidently exactly which columns are features for drift analysis.
    # Exclude 'target' from features always.
    # Exclude 'prediction' from features too, especially for `reference_data` where it doesn't exist.

    # Identify all feature columns present in the reference data (your training data)
    # Assume 'target' is the only non-feature column in reference_data.
    feature_columns_for_drift = [col for col in reference_data.columns if col != "target"]

    # Now, construct the ColumnMapping.
    # - `target`: always specify if present and relevant.
    # - `prediction`: You want to tell Evidently *not* to treat 'prediction' as a core
    #   column for comparison across both datasets IF it's not present in one.
    #   For DataDriftPreset, it primarily cares about the features.
    #   The 'prediction' column in `current_data` will then be treated as just another column/feature in `current_data`.

    column_mapping = ColumnMapping(
        target="target",
        # Explicitly define numerical and/or categorical features for drift analysis.
        # This prevents Evidently from trying to infer features from all columns,
        # which might include 'prediction' when it's not consistently present.
        numerical_features=feature_columns_for_drift, # Assuming all your features are numerical
        categorical_features=[], # Add your actual categorical features here if any
        # Do NOT set `prediction` in ColumnMapping if you only want DataDriftPreset
        # and 'prediction' is not in `reference_data`.
        # If set to None, Evidently will not try to find it for model metrics.
        prediction=None, # Explicitly tell Evidently that no single prediction column is globally consistent
        task=None # Keep this set to None, as we are not evaluating a model task directly here
    )

    data_drift_report = Report(metrics=[
        DataDriftPreset(), # This preset will now analyze only the defined `numerical_features` and `categorical_features`
    ])

    data_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping # Pass the refined ColumnMapping
    )

    data_drift_report.save_html(report_path)

    print(f"✅ Evidently AI report generated at {report_path}")
