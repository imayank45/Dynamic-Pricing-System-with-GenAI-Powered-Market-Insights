from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import yaml
from src.utils.logger import setup_logger

app = FastAPI()
logger = setup_logger("config/config.yaml")

class RetailData(BaseModel):
    product_id: str
    unit_price: float
    comp_1: float
    comp_2: float
    comp_3: float
    qty: int
    product_category_name: str
    product_score: float
    volume: float
    lag_price: float

@app.post("/preprocess")
async def preprocess(data: RetailData):
    """Preprocess retail data for pricing model."""
    logger.info(f"Preprocessing data for product: {data.product_id}")
    
    try:
        # Feature engineering
        avg_comp_price = (data.comp_1 + data.comp_2 + data.comp_3) / 3
        price_gap = data.unit_price - avg_comp_price
        normalized_price = data.unit_price / 1000.0  # Assume max price = 1000
        demand_signal = data.qty / 1000.0  # Assume max qty = 1000
        price_trend = data.unit_price - data.lag_price
        
        features = {
            "product_id": data.product_id,
            "price_gap": price_gap,
            "normalized_price": normalized_price,
            "demand_signal": demand_signal,
            "price_trend": price_trend,
            "product_category_name": data.product_category_name,
            "product_score": data.product_score
        }
        logger.info("Preprocessing completed successfully")
        return features
    
    except Exception as e:
        logger.error(f"Preprocessing failed: {str(e)}")
        raise

if __name__ == "__main__":
    import uvicorn
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    uvicorn.run(app, host=config["api"]["host"], port=config["api"]["port"])