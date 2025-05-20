import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import numpy as np
import gymnasium as gym  # Use gymnasium instead of gym
from gymnasium.spaces import Box  # Use gymnasium.spaces
import pandas as pd
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import yaml
import os
from src.utils.logger import setup_logger
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

# Load environment variables from .env file
load_dotenv()

class RetailPricingEnv(gym.Env):  # Inherit from gymnasium.Env
    """Custom environment for retail pricing using dataset features."""
    def __init__(self, env_config: dict):
        super().__init__()
        # State: [price_gap, normalized_price, demand_signal, price_trend, product_score]
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)
        # Action: Price adjustment factor (-10% to +10%)
        self.action_space = Box(low=-0.1, high=0.1, shape=(1,), dtype=np.float32)
        
        # Dataset features from Parquet file
        self.dataset = env_config.get("dataset")
        self.current_row = None
        self.unit_price = None
        self.qty = None
        self.features = None
        self.step_count = 0
        self.max_steps = 100

        # Initialize with a random product
        self._sample_product()

    def _sample_product(self):
        """Sample a random product from the dataset."""
        self.current_row = self.dataset.sample(n=1).iloc[0]
        self.unit_price = self.current_row["unit_price"]
        self.qty = self.current_row["qty"]
        
        # Compute features (same as preprocess.py)
        avg_comp_price = (self.current_row["comp_1"] + self.current_row["comp_2"] + self.current_row["comp_3"]) / 3
        self.features = {
            "price_gap": self.unit_price - avg_comp_price,
            "normalized_price": self.unit_price / 1000.0,  # Assume max price = 1000
            "demand_signal": self.qty / 1000.0,  # Assume max qty = 1000
            "price_trend": self.unit_price - self.current_row["lag_price"],
            "product_score": self.current_row["product_score"]
        }

    def reset(self, seed=None, options=None):
        """Reset environment with a new product."""
        super().reset(seed=seed)  # Call the parent reset method to handle seeding
        self._sample_product()
        self.current_state = np.array([
            self.features["price_gap"],
            self.features["normalized_price"],
            self.features["demand_signal"],
            self.features["price_trend"],
            self.features["product_score"]
        ], dtype=np.float32)
        self.step_count = 0
        info = {}  # Additional info (empty for now)
        return self.current_state, info  # Gymnasium requires (observation, info)

    def step(self, action):
        """Take a step in the environment."""
        # Apply price adjustment directly
        price_adjustment = action[0]  # Already in range [-0.1, 0.1]
        self.unit_price *= (1 + price_adjustment)
        
        # Update normalized_price
        self.features["normalized_price"] = self.unit_price / 1000.0
        
        # Simulate demand response (higher price reduces qty)
        demand_factor = 1 - (price_adjustment * 0.5)  # Higher price lowers demand
        self.qty = max(1, int(self.qty * demand_factor))
        self.features["demand_signal"] = self.qty / 1000.0
        
        # Update state
        self.current_state = np.array([
            self.features["price_gap"],
            self.features["normalized_price"],
            self.features["demand_signal"],
            self.features["price_trend"],
            self.features["product_score"]
        ], dtype=np.float32)
        
        # Calculate reward (profit: qty * (unit_price - cost))
        cost = self.unit_price * 0.7  # Assume 70% cost
        reward = self.qty * (self.unit_price - cost)
        
        # Check if done
        self.step_count += 1
        terminated = self.step_count >= self.max_steps  # Episode ends when max steps reached
        truncated = False  # No truncation condition (e.g., timeout) in this environment
        
        info = {}  # Additional info (empty for now)
        return self.current_state, reward, terminated, truncated, info  # Gymnasium requires (obs, reward, terminated, truncated, info)

def load_dataset(config_path: str) -> pd.DataFrame:
    """Load dataset from Azure Blob Storage (Parquet file)."""
    logger = setup_logger(config_path)
    logger.info("Loading dataset from Azure Blob Storage (Parquet)")
    
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
        # Define the path to the Parquet file
        container_name = "retail-data"
        blob_path = "delta/retail/processed_data.parquet"
        
        logger.info(f"Downloading Parquet file from {container_name}/{blob_path}")
        blob_client = blob_service_client.get_blob_client(
            container=container_name,
            blob=blob_path
        )
        blob_data = blob_client.download_blob()
        with open("temp_processed_data.parquet", "wb") as temp_file:
            temp_file.write(blob_data.readall())
        
        # Read Parquet into pandas DataFrame
        logger.info("Reading Parquet into pandas DataFrame")
        pandas_df = pd.read_parquet("temp_processed_data.parquet")
        logger.info("Dataset loaded successfully")
        return pandas_df
    
    except Exception as e:
        logger.error(f"Failed to load dataset: {str(e)}")
        raise
    
    finally:
        # Clean up temporary file
        temp_file_path = "temp_processed_data.parquet"
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            logger.info(f"Cleaned up temporary file: {temp_file_path}")

def train_pricing_model(config_path: str) -> None:
    """Train PPO model for dynamic pricing using Stable Baselines3."""
    logger = setup_logger(config_path)
    logger.info("Starting pricing model training")
    
    # Load configuration
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Load dataset
    dataset = load_dataset(config_path)
    
    # Initialize the environment
    env = RetailPricingEnv(env_config={"dataset": dataset})
    
    # Validate the environment
    logger.info("Validating the environment")
    check_env(env)
    logger.info("Environment validation passed")
    
    try:
        # Initialize PPO model with Stable Baselines3
        model = PPO(
            policy="MlpPolicy",  # Use a multi-layer perceptron policy
            env=env,
            learning_rate=5e-4,
            n_steps=2048,  # Number of steps to run for each environment per update
            batch_size=64,
            n_epochs=10,  # Number of epochs per update
            verbose=1,  # Log training progress
            device="auto"  # Automatically select CPU/GPU
        )
        
        # Train the model
        total_timesteps = config["model"]["sac"]["training_iterations"] * 1000  # Convert iterations to timesteps
        logger.info(f"Training PPO model for {total_timesteps} timesteps")
        model.learn(total_timesteps=total_timesteps)
        
        # Save the model
        os.makedirs("models", exist_ok=True)
        model.save("models/ppo_model")
        logger.info("Model training completed and saved successfully")
    
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise

if __name__ == "__main__":
    train_pricing_model("config/config.yaml")