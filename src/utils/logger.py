import logging
import yaml
import os

def setup_logger(config_path: str) -> logging.Logger:
    """Set up logging based on config file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    log_level = getattr(logging, config["logging"]["level"], logging.INFO)
    log_file = config["logging"]["file"]
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger("DynamicPricing")
    logger.setLevel(log_level)
    
    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger