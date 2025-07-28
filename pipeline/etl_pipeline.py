# pipeline/etl_pipeline.py

from zenml import pipeline # Corrected import
from steps.ingest_data import ingest_data_step
from steps.clean_data import clean_data_step
from steps.train_model import train_model_step
from steps.evaluate_model import evaluate_model_step
from steps.generate_predictions import generate_predictions_step
from evidently_report import evidently_report_step # Import the new step

@pipeline
def etl_pipeline():
    # Call the steps directly. ZenML handles the data flow.
    df = ingest_data_step()
    cleaned_df = clean_data_step(df=df)

    # Note: For Evidently, you often want to compare the original cleaned_df
    # (as 'reference_data') with the data that went into production/prediction
    # (as 'current_data', which is your predicted_df).
    # The 'target' column must be present in both for full data/model quality reports.

    model = train_model_step(df=cleaned_df)
    evaluate_model_step(df=cleaned_df, model=model)
    predicted_df = generate_predictions_step(input_df=cleaned_df) # Capture the output

    # Add the Evidently AI report generation step
    evidently_report_step(reference_data=cleaned_df, current_data=predicted_df)

if __name__ == "__main__":
    my_pipeline = etl_pipeline()
    my_pipeline.run()
