# run_pipeline.py

from pipeline.etl_pipeline import etl_pipeline

if __name__ == "__main__":
    # Instantiate the pipeline and then call .run() on the instance.
    # etl_pipeline is now a class, so you instantiate it like this:
    my_pipeline = etl_pipeline()
    
