import os
from dotenv import load_dotenv
from openai import OpenAI

# Clear existing OPENAI_API_KEY
if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]
    print("Cleared existing OPENAI_API_KEY")

# Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Load .env with verbose output
env_path = os.path.join(os.getcwd(), ".env")
dotenv_loaded = load_dotenv(dotenv_path=env_path, verbose=True)
print(f".env file loaded successfully: {dotenv_loaded}")
print(f".env file exists: {os.path.exists(env_path)}")

# Debugging: list all environment variables containing 'OPENAI'
print("All env variables containing 'OPENAI':")
for k, v in os.environ.items():
    if "OPENAI" in k:
        print(f"{k} = {v[:20]}...")

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    print("Error: OPENAI_API_KEY not found in environment variables")
    exit(1)
print(f"Loaded API Key: {api_key[:20]}...")

# Confirm the key is valid
try:
    client = OpenAI(api_key=api_key)
    models = client.models.list()
    print("Available models:", [m.id for m in models.data])
except Exception as e:
    print(f"Error during API call: {e}")
    exit(1)