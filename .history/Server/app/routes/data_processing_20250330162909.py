    from fastapi import APIRouter, HTTPException
    from pydantic import BaseModel
    import asyncio
    from ..services.groq_service import process_groq_data, process_groq_data_async

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
            
            # Use the async version of the service function
            result = await process_groq_data_async(input_dict)
            return result
        except HTTPException as e:
            # Pass through HTTPException with its status code
            raise e
        except Exception as e:
            # Log the exception for debugging
            print(f"Error in process_data endpoint: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")