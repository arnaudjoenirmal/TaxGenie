from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services import groq_service

router = APIRouter()

class InputData(BaseModel):
    account_info: dict
    transactions: list

@router.post("/process_data/")
async def process_data(input_data: InputData):
    """
    Accepts JSON input, sends it to the Groq API, and returns the processed output.
    """
    try:
        # Convert Pydantic model to dictionary
        input_dict = input_data.model_dump()
        
        # Make sure we're properly awaiting the async function
        result = await groq_service.process_groq_data(input_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")