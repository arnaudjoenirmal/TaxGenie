import os
import requests
from fastapi import HTTPException

# Store API key securely (use environment variables)
GROQ_API_KEY = "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"  # Set this in your environment
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def process_groq_data(input_data: dict):
    """
    Sends input data to the Groq API and returns the processed response.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",  # Choose a model from Groq's available models
        "messages": [
            {"role": "system", "content": "Preprocess the data and extract necessary details for tax calculations."},
            {"role": "user", "content": str(input_data)}
        ],
        "temperature": 0.7,  # Adjust as needed
        "max_tokens": 500  # Adjust token limit
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for non-200 responses
        return response.json()  # Return the response data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Groq API request failed: {str(e)}")
