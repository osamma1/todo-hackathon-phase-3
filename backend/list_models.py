import sys
import os
import cohere
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
api_key = os.getenv("COHERE_API_KEY")

try:
    client = cohere.Client(api_key=api_key)
    models = client.models.list()
    print("Available Models:")
    for model in models.models:
        print(f"- {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
