import requests
from fastapi import HTTPException

groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
groq_api_key = "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"  # Store this securely

def process_groq_data(input_data: dict):
    """
    This function sends input data to the Groq API and returns the processed response.
    """
    data_to_send = {
        "model": "llama3-8b",  # Specify the correct model
        "messages": [
            {"role": "system", "content": "You are an AI assistant specialized in tax calculations."},
            {"role": "user", "content": f"Extract tax-relevant information from this data: {input_data}"}
        ],
        "temperature": 0.7
    }
    
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(groq_api_url, json=data_to_send, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the JSON response from Groq
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Groq API error: {response.text}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request to Groq API failed: {str(e)}")
