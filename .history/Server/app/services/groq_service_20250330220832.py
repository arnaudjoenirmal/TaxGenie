import os
import json
import logging
import httpx
from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import Dict, List, Any


GROQ_API_KEY = "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" #API 
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
            {"role": "system", "content": "Extract key-value pairs, transactions, and a financial summary from the input data. Format the output as structured JSON."},
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
            return response.json()
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

class FinancialData(BaseModel):
    key_value_pairs: Dict[str, Any]
    tables: List[List[List[Any]]]

@router.post("/process_data/")
async def process_data(input_data: FinancialData):
    """
    This endpoint accepts JSON input, sends it to the Groq API asynchronously, and returns the processed output.
    """
    try:
        raw_result = await process_groq_data(input_data.dict())
        
        if isinstance(raw_result, str):
            processed_result = json.loads(raw_result)
        else:
            processed_result = raw_result
        
        return processed_result
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse Groq API response as JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


