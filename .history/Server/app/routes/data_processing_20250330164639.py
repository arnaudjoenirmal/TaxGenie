from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
from ..services import groq_service

router = APIRouter()

class FinancialData(BaseModel):
    key_value_pairs: Dict[str, Any]  # Dictionary for account details
    tables: List[List[List[Any]]]  # Nested lists for table structure

@router.post("/process_data/")
async def process_data(input_data: FinancialData):
    """
    This endpoint accepts the JSON input, sends it to the Groq API, and returns the processed output.
    """
    try:
        # Debugging: Print received data
        print(f"Received data: {input_data}")

        # Convert Pydantic model to dictionary
        result = groq_service.process_groq_data(input_data.model_dump())  
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
