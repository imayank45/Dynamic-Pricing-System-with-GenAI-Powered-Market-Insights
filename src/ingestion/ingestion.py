import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession
import yaml
from src.utils.logger import setup_logger
import time

# Load environment variables from .env file
load_dotenv()

def ingest_data(config_path: str) -> None:
    """Ingest retail data into Delta table."""
    logger = setup_logger(config_path)
    logger.info("Starting data ingestion pipeline")
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    spark = (
        SparkSession.builder
        .appName(config["spark"]["app_name"])
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.3.0,org.apache.hadoop:hadoop-azure:3.3.1,com.microsoft.azure:azure-storage:8.6.6")
        .config("spark.local.dir", "C:/ds_projects/spark-temp")
        .getOrCreate()
    )
    
    # Get connection string from environment variable
    connection_string = os.getenv("AZURE_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("AZURE_CONNECTION_STRING environment variable not set")
    
    # Set Azure Blob Storage authentication
    spark._jsc.hadoopConfiguration().set(
        f"fs.azure.account.key.{config['azure']['storage_account']}.blob.core.windows.net",
        connection_string.split("AccountKey=")[1].split(";")[0]
    )
    
    try:
        data_path = f"wasbs://{config['azure']['container']}@{config['azure']['storage_account']}.blob.core.windows.net/retail_price.csv"
        logger.info(f"Reading data from {data_path}")
        
        data = spark.read.csv(data_path, header=True, inferSchema=True)
        
        # Select relevant columns
        selected_columns = [
            "product_id", "unit_price", "comp_1", "comp_2", "comp_3", "qty",
            "product_category_name", "month_year", "product_score", "volume", "lag_price"
        ]
        data = data.select(selected_columns)
        
        delta_path = config["spark"]["delta_table"]
        logger.info(f"Writing to Delta table: {delta_path}")
        
        data.write.mode("overwrite").format("delta").save(delta_path)
        logger.info("Data ingestion completed successfully")
    
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise
    
    finally:
        spark.stop()
        time.sleep(5)

if __name__ == "__main__":
    ingest_data("config/config.yaml")