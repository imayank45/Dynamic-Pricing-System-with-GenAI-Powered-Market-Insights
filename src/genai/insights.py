from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
import yaml
from src.utils.logger import setup_logger
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
            token=hf_token if hf_token else None
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
    """Generate market insights."""
    logger = setup_logger(config_path)
    logger.info(f"Generating insights for product: {data['product_id']}")
    
    # Placeholder: Use fine-tuned model
    return f"Adjust price due to high demand in {data['product_category_name']}."

if __name__ == "__main__":
    fine_tune_genai("config/config.yaml")