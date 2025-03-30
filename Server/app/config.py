import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Get API keys and URLs from environment variables
GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
