from fastapi import APIRouter, HTTPException
from ..services import groq_service
from pydantic import BaseModel

router = APIRouter()

class InputData(BaseModel):
    account_info: dict
    transactions: list

@router.post("/process_data/")
async def process_data(input_data: InputData):
    """
    This endpoint accepts the JSON input, sends it to the Groq API, and returns the processed output.
    """
    try:
        # Call the Groq API service
        result = groq_service.process_groq_data(input_data.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
