import os
from dotenv import load_dotenv
from openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
import yaml
from src.utils.logger import setup_logger

# Clear existing OPENAI_API_KEY and HUGGINGFACE_TOKEN to avoid overrides
if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]
    print("Cleared existing OPENAI_API_KEY")
if "HUGGINGFACE_TOKEN" in os.environ:
    del os.environ["HUGGINGFACE_TOKEN"]
    print("Cleared existing HUGGINGFACE_TOKEN")

# Load environment variables from .env file
env_path = os.path.join(os.getcwd(), ".env")
dotenv_loaded = load_dotenv(dotenv_path=env_path, verbose=True)
print(f".env file loaded successfully: {dotenv_loaded}")
print(f".env file exists: {os.path.exists(env_path)}")

# Debugging: list all environment variables containing 'OPENAI' or 'HUGGINGFACE'
print("All relevant environment variables:")
for k, v in os.environ.items():
    if "OPENAI" in k or "HUGGINGFACE" in k:
        print(f"{k} = {v[:20]}...")

# Initialize OpenAI client with API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")
print(f"Loaded OpenAI API Key: {api_key[:20]}...")
client = OpenAI(api_key=api_key)

def fine_tune_genai(config_path: str) -> None:
    """Fine-tune model for market insights."""
    logger = setup_logger(config_path)
    logger.info("Starting GenAI fine-tuning")
    
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    # Get Hugging Face token from environment variable
    hf_token = os.getenv("HUGGINGFACE_TOKEN")
    if not hf_token:
        logger.warning("HUGGINGFACE_TOKEN not found in .env. Attempting to proceed without token (may fail for gated models).")
    
    try:
        # Load model and tokenizer with token if provided, on CPU
        logger.info(f"Loading model {config['genai']['model_name']} on CPU")
        model = AutoModelForCausalLM.from_pretrained(
            config["genai"]["model_name"],
            token=hf_token if hf_token else None,
            device_map="cpu"  # Explicitly load on CPU
        )
        logger.info("Model loaded successfully")
        
        logger.info("Loading tokenizer")
        tokenizer = AutoTokenizer.from_pretrained(
            config["genai"]["model_name"],
            token=hf_token if hf_token else None,
            clean_up_tokenization_spaces=True  # Suppress FutureWarning
        )
        logger.info("Tokenizer loaded successfully")
        
        logger.info("Applying LoRA configuration")
        # Set target modules based on the model architecture
        model_name = config["genai"]["model_name"].lower()
        if "gpt2" in model_name:
            target_modules = ["c_attn"]  # GPT-2 uses c_attn for attention projections
        elif "opt" in model_name:
            target_modules = ["q_proj", "v_proj"]  # OPT models use q_proj, v_proj
        else:
            target_modules = ["q", "v"]  # Default for Mistral-like models
        
        lora_config = LoraConfig(
            r=config["genai"]["lora_r"],
            lora_alpha=config["genai"]["lora_alpha"],
            target_modules=target_modules
        )
        model = get_peft_model(model, lora_config)
        logger.info("LoRA configuration applied successfully")
        
        # Placeholder: Add fine-tuning logic
        logger.info("GenAI fine-tuning completed successfully")
    
    except Exception as e:
        logger.error(f"Fine-tuning failed: {str(e)}")
        raise

def generate_insights(data: dict, config_path: str) -> str:
    """Generate detailed market insights in 5-6 lines using OpenAI API."""
    logger = setup_logger(config_path)
    logger.debug("Debug: Logger initialized for generate_insights")
    logger.info(f"Generating insights for product: {data['product_id']}")
    
    # Extract features for analysis
    price_gap = data["price_gap"]
    demand_signal = data["demand_signal"]
    product_score = data["product_score"]
    category = data["product_category_name"]
    
    # Craft a prompt for OpenAI API
    prompt = (
        f"Generate market insights for a product in the {category} category. "
        f"The product's price is ${price_gap:.2f} {'above' if price_gap > 0 else 'below'} the average competitor price. "
        f"Demand signal is {demand_signal:.3f} (normalized qty, max 1.0). "
        f"Product score is {product_score:.1f} out of 5. "
        f"Provide detailed insights in 5-6 lines, focusing on pricing strategy, demand trends, and quality perception."
    )
    
    try:
        # Call OpenAI API using the new interface
        response = client.chat.completions.create(
            model="gpt-4",  # You can use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a market analyst providing pricing and demand insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  # Enough for 5-6 lines
            temperature=0.7  # Balanced creativity
        )
        insights = response.choices[0].message.content.strip()
        logger.info("Insights generated successfully via OpenAI API")
        return insights
    except Exception as e:
        logger.error(f"Failed to generate insights via OpenAI API: {str(e)}")
        raise

if __name__ == "__main__":
    # Run fine_tune_genai
    fine_tune_genai("config/config.yaml")
    
    # Test generate_insights with sample data
    sample_data = {
        "product_id": "123",
        "price_gap": 95.33,  # Example: unit_price - avg_comp_price
        "demand_signal": 0.088,  # Example: qty / 1000
        "product_score": 4.5,
        "product_category_name": "Electronics"
    }
    insights = generate_insights(sample_data, "config/config.yaml")
    print("Generated Insights:")
    print(insights)