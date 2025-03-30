# # from fastapi import APIRouter, HTTPException
# # from pydantic import BaseModel
# # from typing import Dict, List, Any
# # from ..services import groq_service

# # router = APIRouter()

# # class FinancialData(BaseModel):
# #     key_value_pairs: Dict[str, Any]  # Dictionary for account details
# #     tables: List[List[List[Any]]]  # Nested lists for table structure

# # @router.post("/process_data/")
# # async def process_data(input_data: FinancialData):
# #     """
# #     This endpoint accepts the JSON input, sends it to the Groq API, and returns the processed output.
# #     """
# #     try:
# #         # Debugging: Print received data
# #         print(f"Received data: {input_data}")

# #         # Convert Pydantic model to dictionary
# #         result = groq_service.process_groq_data(input_data.model_dump())  
# #         return result
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Dict, List, Any
# from ..services import groq_service
# import json

# router = APIRouter()

# class FinancialData(BaseModel):
#     key_value_pairs: Dict[str, Any]  # Dictionary for account details
#     tables: List[List[List[Any]]]  # Nested lists for table structure

# @router.post("/process_data/")
# async def process_data(input_data: FinancialData):
#     """
#     This endpoint accepts the JSON input, sends it to the Groq API, and returns the processed output.
#     """
#     try:
#         # Convert Pydantic model to dictionary
#         raw_result = groq_service.process_groq_data(input_data.model_dump())

#         # Ensure response is parsed correctly
#         if isinstance(raw_result, str):
#             processed_result = json.loads(raw_result)  # Convert string to JSON
#         else:
#             processed_result = raw_result  # Already in JSON format

#         return processed_result

#     except json.JSONDecodeError:
#         raise HTTPException(status_code=500, detail="Failed to parse Groq API response as JSON")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any
from ..services.groq_service import process_groq_data  # Import the async function
import json
import re

router = APIRouter()

class FinancialData(BaseModel):
    key_value_pairs: Dict[str, Any]  # Dictionary for account details
    tables: List[List[List[Any]]]  # Nested lists for table structure

class RawGroqResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, Any]



@router.post("/process_data/")
async def process_data(input_data: FinancialData):
    """
    Accepts JSON input, sends it to the Groq API asynchronously, and returns the processed output.
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

class GroqResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, Any]

def clean_json_string(json_string: str) -> str:
    """Removes Markdown-style formatting and unnecessary newlines."""
    return re.sub(r"```json|```", "", json_string).strip()

@router.post("/convert_groq_output/")
async def convert_groq_output(input_data: GroqResponse):
    """
    Extracts structured JSON content from a Groq API response.
    """
    try:
        # Extract response content
        raw_content = input_data.choices[0]["message"]["content"]
        
        # Log the raw response for debugging
        logger.info(f"Raw Groq Response: {raw_content}")

        # Clean the response
        cleaned_content = clean_json_string(raw_content)
        
        # Log the cleaned response before parsing
        logger.info(f"Cleaned JSON Content: {cleaned_content}")

        # Convert to dictionary
        structured_result = json.loads(cleaned_content)

        return structured_result

    except json.JSONDecodeError:
        logger.error("JSON Decode Error: The response is not valid JSON.")
        raise HTTPException(status_code=500, detail="Failed to parse extracted JSON content. Ensure the response is valid JSON.")
    except KeyError:
        logger.error("Key Error: Unexpected response format from Groq API.")
        raise HTTPException(status_code=500, detail="Unexpected response format from Groq API.")
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")