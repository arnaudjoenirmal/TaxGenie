# import os
# import json
# import requests
# from fastapi import HTTPException

# # Store API key securely (use environment variables in production)
# GROQ_API_KEY = "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"
# GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# def process_groq_data(input_data: dict):
#     """
#     Sends input data to the Groq API and returns the processed response.
#     Includes detailed error handling and logging.
#     """
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     # Properly serialize the input data to avoid formatting issues
#     user_content = json.dumps(input_data, default=str)
    
#     payload = {
#         "model": "llama3-70b-8192",  # Using a current Groq model
#         "messages": [
#             {"role": "system", "content": "Preprocess the data and extract necessary details for tax calculations."},
#             {"role": "user", "content": user_content}
#         ],
#         "temperature": 0.7,
#         "max_tokens": 500
#     }
    
#     try:
#         print(f"Sending request to Groq with payload: {payload}")
#         response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        
#         # Get the response content regardless of status code
#         response_content = response.text
#         print(f"Groq API response status: {response.status_code}")
#         print(f"Groq API response content: {response_content}")
        
#         # Then check status code and raise appropriate exception
#         if response.status_code != 200:
#             raise HTTPException(
#                 status_code=response.status_code,
#                 detail=f"Groq API error ({response.status_code}): {response_content}"
#             )
            
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Request exception: {str(e)}")
#         if hasattr(e, 'response') and e.response:
#             print(f"Response content: {e.response.text}")
#             error_detail = f"{str(e)} - Response: {e.response.text}"
#         else:
#             error_detail = str(e)
#         raise HTTPException(status_code=500, detail=f"Groq API request failed: {error_detail}")
#     except Exception as e:
#         print(f"Unexpected error: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# # If you need an async version of this function for use with FastAPI
# async def process_groq_data_async(input_data: dict):
#     """
#     Async wrapper for the Groq API service.
#     """
#     import asyncio
#     return await asyncio.to_thread(process_groq_data, input_data)



import os
import json
import requests
from fastapi import HTTPException

# Store API key securely (use environment variables in production)
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def process_groq_data(input_data: dict):
    """
    Sends input data to the Groq API and returns only the processed content as JSON.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Modify the system prompt to request JSON output
    system_message = """
    Your task is to extract tax-relevant information from the input data and return ONLY a valid JSON object.
    Do not include any explanations, markdown formatting, or backticks.
    """
    
    # Properly serialize the input data
    user_content = json.dumps(input_data, default=str)
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.2,  # Lower temperature for more consistent output
        "max_tokens": 800
    }
    
    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        
        # Handle non-200 responses
        if response.status_code != 200:
            response_content = response.text
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Groq API error ({response.status_code}): {response_content}"
            )
        
        # Parse the response    
        response_json = response.json()
        
        # Extract just the content from the response
        if 'choices' in response_json and len(response_json['choices']) > 0:
            content = response_json['choices'][0]['message']['content']
            
            # Try to parse the content as JSON
            try:
                # Parse the content string into a JSON object
                parsed_json = json.loads(content)
                return parsed_json  # Return just the parsed JSON content
            except json.JSONDecodeError:
                # If the content isn't valid JSON, wrap it in a simple JSON structure
                return {"extracted_text": content}
        else:
            raise HTTPException(
                status_code=500,
                detail="No content found in the Groq API response"
            )
            
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")
        if hasattr(e, 'response') and e.response:
            error_detail = f"{str(e)} - Response: {e.response.text}"
        else:
            error_detail = str(e)
        raise HTTPException(status_code=500, detail=f"Groq API request failed: {error_detail}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Async wrapper for FastAPI
async def process_groq_data_async(input_data: dict):
    """
    Async wrapper for the Groq API service.
    """
    import asyncio
    return await asyncio.to_thread(process_groq_data, input_data)