import cohere
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client
cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))