import requests
from fastapi import HTTPException

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def process_groq_data(input_data: dict):
    """
    Sends input data to the Groq API and returns the processed response.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # More explicit message formatting
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "Preprocess the data and extract necessary details for tax calculations."},
            {"role": "user", "content": str(input_data)}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        # Print the payload for debugging
        print(f"Sending payload: {payload}")
        
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        
        # More detailed error handling
        if response.status_code != 200:
            print(f"Error response: {response.text}")
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Groq API error: {response.text}"
            )
            
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Groq API request failed: {str(e)}")