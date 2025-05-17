from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yaml
from src.preprocessing.preprocess import preprocess
from src.genai.insights import generate_insights
from src.utils.logger import setup_logger

app = FastAPI()
logger = setup_logger("config/config.yaml")

class PricingRequest(BaseModel):
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

    # Add Pydantic configuration to coerce types
    class Config:
        # Allow string-to-number coercion (e.g., "180" -> 180.0)
        coerce_numbers_to_str = False
        # Log raw request data for debugging
        @staticmethod
        def schema_extra(schema, model):
            logger.info(f"Expected schema: {schema}")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the Dynamic Pricing API. Use /docs to test the endpoints."}

@app.post("/predict_price")
async def predict_price(request: PricingRequest):
    """Predict optimal price."""
    # Log the incoming request for debugging
    logger.info(f"Received request: {request.dict()}")
    logger.info(f"Predicting price for product: {request.product_id}")
    try:
        # Preprocess data
        features = await preprocess(request)
        
        # Placeholder: Call SAC model (replace with actual PPO model logic if needed)
        recommended_price = request.unit_price * 1.1  # Dummy logic
        logger.info("Price prediction completed")
        return {
            "product_id": request.product_id,
            "recommended_price": recommended_price,
            "features": features
        }
    except Exception as e:
        logger.error(f"Price prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Price prediction failed: {str(e)}")

@app.post("/generate_insights")
async def generate_insights_endpoint(request: PricingRequest):
    """Generate market insights."""
    logger.info(f"Generating insights for product: {request.product_id}")
    try:
        features = await preprocess(request)
        insights = generate_insights(features, "config/config.yaml")
        logger.info("Insights generation completed")
        return {"product_id": request.product_id, "insights": insights}
    except Exception as e:
        logger.error(f"Insights generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    with open("config/config.yaml", "r") as file:
        config = yaml.safe_load(file)
    uvicorn.run(app, host=config["api"]["host"], port=config["api"]["port"])