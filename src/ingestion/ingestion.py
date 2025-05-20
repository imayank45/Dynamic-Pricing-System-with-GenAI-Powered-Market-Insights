import logging
from pyspark.sql import SparkSession
import yaml
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DynamicPricing")

def get_spark_session():
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable not set")

    spark = (SparkSession.builder
             .appName("RetailIngestion")
             # Explicitly set all Hadoop dependencies to 3.3.6
             .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.1.0,org.apache.hadoop:hadoop-azure:3.3.6,org.apache.hadoop:hadoop-common:3.3.6,org.apache.hadoop:hadoop-client:3.3.6")
             .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
             .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
             .config("spark.hadoop.fs.azure.account.key.retaildynamic.blob.core.windows.net", 
                     connection_string.split("AccountKey=")[1].split(";")[0])
             .getOrCreate())
    return spark

def ingest_data(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    data_path = config['data']['path']
    delta_path = config['spark']['delta_table']
    selected_columns = config['data']['selected_columns']
    
    logger.info(f"Reading data from {data_path}")
    spark = get_spark_session()
    
    try:
        data = spark.read.csv(data_path, header=True, inferSchema=True)
        data = data.select(selected_columns)
        logger.info(f"Writing to Delta table: {delta_path}")
        data.write.format("delta").mode("overwrite").save(delta_path)
        logger.info("Data ingestion completed successfully")
        
        # Preview the ingested data
        delta_data = spark.read.format("delta").load(delta_path)
        logger.info("Preview of ingested data:")
        delta_data.show()
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    ingest_data("config/config.yaml")