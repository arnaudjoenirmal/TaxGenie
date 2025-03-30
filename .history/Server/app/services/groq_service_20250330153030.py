import requests
from fastapi import HTTPException

groq_api_url = "https://api.groq.com/openai/v1/chat/completions
"
groq_api_key = "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"  # It’s a good idea to store this in a config or environment variable

def process_groq_data(input_data: dict):
    """
    This function sends input data to the Groq API and returns the processed response.
    """
    data_to_send = {
        "prompt": "Preprocess the data and extract the necessary data for tax calculations",
        "input_data": input_data
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
