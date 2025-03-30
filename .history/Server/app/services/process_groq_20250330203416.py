import os
import json
import logging
import httpx
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import Dict, List, Any

# Securely store API key in environment variables
GROQ_API_KEY = "your_groq_api_key"  # Replace with your actual key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_groq_data(input_data: dict):
    """
    Sends input data to the Groq API asynchronously and returns the processed response.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    user_content = json.dumps(input_data, default=str)
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "Extract key-value pairs, transactions, and a financial summary from the input JSON. Return the output as structured JSON."},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.7,
        "max_tokens": 1500
    }

    try:
        logger.info("Sending request to Groq API...")
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, json=payload, headers=headers)

        logger.info(f"Groq API Response Status: {response.status_code}")

        if response.status_code == 200:
            response_json = response.json()
            raw_content = response_json["choices"][0]["message"]["content"]

            # Extract JSON content from the response
            try:
                extracted_data = json.loads(raw_content)
                return extracted_data
            except json.JSONDecodeError:
                logger.error("Failed to parse JSON from API response")
                raise HTTPException(status_code=500, detail="Invalid JSON format in response")
        
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            logger.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            return {"error": "Rate limit exceeded. Please try again later."}
        else:
            error_message = f"Groq API error ({response.status_code}): {response.text}"
            logger.error(error_message)
            raise HTTPException(status_code=response.status_code, detail=error_message)
    
    except httpx.RequestError as e:
        error_detail = f"Request failed: {str(e)}"
        logger.error(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# FastAPI Router
router = APIRouter()

class RawGroqResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, Any]

@router.post("/convert_groq_output/")
async def convert_groq_output(input_data: RawGroqResponse):
    """
    This endpoint takes the raw Groq response JSON, extracts structured data, and returns the cleaned JSON.
    """
    try:
        structured_result = await process_groq_data(input_data.dict())
        return structured_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
