import os
from dotenv import load_dotenv
import pandas as pd
from azure.storage.blob import BlobServiceClient
import yaml
from src.utils.logger import setup_logger

# Load environment variables from .env file
load_dotenv()

def ingest_data(config_path: str) -> None:
    """Ingest retail data into Azure Blob Storage using pandas."""
    logger = setup_logger(config_path)
    logger.info("Starting data ingestion pipeline")
    
    # Load configuration
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Get Azure connection string: prioritize .env, fall back to config.yaml
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    if not connection_string:
        connection_string = config["azure"].get("connection_string")
        if not connection_string:
            raise ValueError("AZURE_CONNECTION_STRING not set in .env and azure.connection_string not found in config.yaml")
    
    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    try:
        # Define paths
        container_name = config["azure"]["container"]  # e.g., "retaildata"
        storage_account = config["azure"]["storage_account"]  # e.g., "retaildynamic"
        input_blob_path = "retail_price.csv"
        
        # Extract output container and path from the original delta_table path
        # Original: wasbs://retail-data@retaildynamic.blob.core.windows.net/delta/retail
        output_container_name = "retail-data"
        output_blob_path = "delta/retail/processed_data.parquet"  # Output path in Azure Blob Storage
        
        # Download the CSV file from Azure Blob Storage
        logger.info(f"Downloading data from {container_name}/{input_blob_path}")
        input_blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=input_blob_path
        )
        blob_data = input_blob_client.download_blob()
        with open("temp.csv", "wb") as temp_file:
            temp_file.write(blob_data.readall())
        
        # Read CSV into pandas DataFrame
        logger.info("Reading CSV into pandas DataFrame")
        data = pd.read_csv("temp.csv")
        
        # Select relevant columns
        selected_columns = [
            "product_id", "unit_price", "comp_1", "comp_2", "comp_3", "qty",
            "product_category_name", "month_year", "product_score", "volume", "lag_price"
        ]
        data = data[selected_columns]
        
        # Write the processed data to a temporary Parquet file
        logger.info("Writing processed data to temporary Parquet file")
        temp_output_path = "temp_processed_data.parquet"
        data.to_parquet(temp_output_path, index=False)
        
        # Upload the processed Parquet file to Azure Blob Storage
        logger.info(f"Uploading processed data to {output_container_name}/{output_blob_path}")
        output_blob_client = blob_service_client.get_blob_client(
            container=output_container_name,
            blob=output_blob_path
        )
        with open(temp_output_path, "rb") as data_file:
            output_blob_client.upload_blob(data_file, overwrite=True)
        
        logger.info("Data ingestion completed successfully")
    
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise
    
    finally:
        # Clean up temporary files
        for temp_file in ["temp.csv", "temp_processed_data.parquet"]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                logger.info(f"Cleaned up temporary file: {temp_file}")

if __name__ == "__main__":
    ingest_data("config/config.yaml")