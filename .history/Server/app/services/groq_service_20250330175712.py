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
#         "max_tokens": 1500
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




# # # import os
# # # import json

# # # import requests
# # # from fastapi import HTTPException

# # # # Store API key securely (use environment variables in production)
# # # GROQ_API_KEY = "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"
# # # GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# # # def process_groq_data(input_data: dict):
# # #     """
# # #     Sends input data to the Groq API and returns only the processed content as JSON.
# # #     """
# # #     headers = {
# # #         "Authorization": f"Bearer {GROQ_API_KEY}",
# # #         "Content-Type": "application/json"
# # #     }
    
# # #     # Modify the system prompt to request JSON output
# # #     system_message = """
# # #     Your task is to extract tax-relevant information from the input data and return ONLY a valid JSON object.
# # #     Do not include any explanations, markdown formatting, or backticks.
# # #     """
    
# # #     # Properly serialize the input data
# # #     user_content = json.dumps(input_data, default=str)
    
# # #     payload = {
# # #         "model": "llama3-70b-8192",
# # #         "messages": [
# # #             {"role": "system", "content": system_message},
# # #             {"role": "user", "content": user_content}
# # #         ],
# # #         "temperature": 0.2,  # Lower temperature for more consistent output
# # #         "max_tokens": 800
# # #     }
    
# # #     try:
# # #         response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        
# # #         # Handle non-200 responses
# # #         if response.status_code != 200:
# # #             response_content = response.text
# # #             raise HTTPException(
# # #                 status_code=response.status_code,
# # #                 detail=f"Groq API error ({response.status_code}): {response_content}"
# # #             )
        
# # #         # Parse the response    
# # #         response_json = response.json()
        
# # #         # Extract just the content from the response
# # #         if 'choices' in response_json and len(response_json['choices']) > 0:
# # #             content = response_json['choices'][0]['message']['content']
            
# # #             # Try to parse the content as JSON
# # #             try:
# # #                 # Parse the content string into a JSON object
# # #                 parsed_json = json.loads(content)
# # #                 return parsed_json  # Return just the parsed JSON content
# # #             except json.JSONDecodeError:
# # #                 # If the content isn't valid JSON, wrap it in a simple JSON structure
# # #                 return {"extracted_text": content}
# # #         else:
# # #             raise HTTPException(
# # #                 status_code=500,
# # #                 detail="No content found in the Groq API response"
# # #             )
            
# # #     except requests.exceptions.RequestException as e:
# # #         print(f"Request exception: {str(e)}")
# # #         if hasattr(e, 'response') and e.response:
# # #             error_detail = f"{str(e)} - Response: {e.response.text}"
# # #         else:
# # #             error_detail = str(e)
# # #         raise HTTPException(status_code=500, detail=f"Groq API request failed: {error_detail}")
# # #     except Exception as e:
# # #         print(f"Unexpected error: {str(e)}")
# # #         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# # # # Async wrapper for FastAPI
# # # async def process_groq_data_async(input_data: dict):
# # #     """
# # #     Async wrapper for the Groq API service.
# # #     """
# # #     import asyncio
# # #     return await asyncio.to_thread(process_groq_data, input_data)


# # import os
# # import json
# # import requests
# # from fastapi import HTTPException

# # GROQ_API_KEY = "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"
# # GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# # def process_groq_data(input_data: dict):
# #     """
# #     Sends input data to the Groq API and returns the processed response in structured JSON format.
# #     """
# #     headers = {
# #         "Authorization": f"Bearer {GROQ_API_KEY}",
# #         "Content-Type": "application/json"
# #     }
    
# #     user_content = json.dumps(input_data, default=str)
    
# #     payload = {
# #         "model": "llama3-70b-8192",
# #         "messages": [
# #             {"role": "system", "content": "Preprocess the data and extract necessary details for tax calculations. Respond in structured JSON format without extra explanations."},
# #             {"role": "user", "content": user_content}
# #         ],
# #         "temperature": 0.7,
# #         "max_tokens": 1000
# #     }
    
# #     try:
# #         response = requests.post(GROQ_API_URL, json=payload, headers=headers)
# #         response_content = response.json()
        
# #         if response.status_code != 200:
# #             raise HTTPException(
# #                 status_code=response.status_code,
# #                 detail=f"Groq API error ({response.status_code}): {response_content}"
# #             )
        
# #         # Extract the structured JSON output from the response
# #         structured_response = response_content.get("choices", [{}])[0].get("message", {}).get("content", "{}")
        
# #         return json.loads(structured_response)  # Ensure it's parsed into a Python dictionary
# #     except requests.exceptions.RequestException as e:
# #         raise HTTPException(status_code=500, detail=f"Groq API request failed: {str(e)}")
# #     except json.JSONDecodeError:
# #         raise HTTPException(status_code=500, detail="Failed to decode JSON response from Groq API.")
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# # # Async version for FastAPI
# # async def process_groq_data_async(input_data: dict):
# #     import asyncio
# #     return await asyncio.to_thread(process_groq_data, input_data)

import os
import json
import requests
import re
from fastapi import HTTPException

# Store API key securely (use environment variables in production)
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def process_groq_data(input_data: dict):
    """
    Sends input data to the Groq API and returns only the processed financial data in JSON format.
    Also handles and repairs malformed JSON in error responses.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
   
    # Properly serialize the input data to avoid formatting issues
    user_content = json.dumps(input_data, default=str)
   
    # Simplified system prompt to focus on extracting data only
    system_prompt = """
    Extract financial data from the provided information as JSON with this structure:
    {
        "accountDetails": {
            "accountNo": "string",
            "openingBalance": number
        },
        "transactions": [
            {
                "transDate": "string",
                "reference": "string",
                "debit": number,
                "credit": number,
                "balance": number,
                "remarks": "string"
            }
        ]
    }
    Return ONLY valid JSON without any additional text.
    """
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.1,  # Even lower temperature for more deterministic output
        "max_tokens": 1500
    }
   
    try:
        print(f"Sending request to Groq with payload: {payload}")
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
       
        # Get the response content
        response_content = response.text
        print(f"Groq API response status: {response.status_code}")
        
        # First attempt to process a successful response
        if response.status_code == 200:
            response_json = response.json()
            
            if "choices" in response_json and len(response_json["choices"]) > 0:
                content = response_json["choices"][0]["message"]["content"]
                
                try:
                    # Try to parse the content as JSON
                    financial_data = json.loads(content)
                    return financial_data
                except json.JSONDecodeError:
                    # Look for JSON pattern in the content
                    json_match = re.search(r'({[\s\S]*})', content, re.DOTALL)
                    if json_match:
                        try:
                            financial_data = json.loads(json_match.group(1))
                            return financial_data
                        except json.JSONDecodeError:
                            # Will fall through to error handling below
                            pass
        
        # Handle error responses, focusing on extracting data from json_validate_failed errors
        error_data = {}
        try:
            error_data = json.loads(response_content)
        except json.JSONDecodeError:
            pass
            
        # Check if there's a failed_generation field in the error
        if (error_data and "error" in error_data and 
            "failed_generation" in error_data["error"]):
            
            failed_json = error_data["error"]["failed_generation"]
            
            # Attempt to fix common JSON errors
            # 1. Fix extra closing bracket at the end if present
            if failed_json.strip().endswith("}}"):
                fixed_json = failed_json.strip()[:-1]
                try:
                    return json.loads(fixed_json)
                except json.JSONDecodeError:
                    pass
                    
            # 2. Extract what looks like valid JSON up to a known good property
            json_parts = re.search(r'({[\s\S]*?"transactions":\s*\[[\s\S]*?\])', failed_json)
            if json_parts:
                try:
                    # Add closing bracket and try to parse
                    fixed_json = json_parts.group(1) + "}"
                    return json.loads(fixed_json)
                except json.JSONDecodeError:
                    pass
                    
            # 3. Parse the transactions array directly and rebuild
            trans_match = re.search(r'"transactions":\s*(\[[\s\S]*?\])', failed_json)
            if trans_match:
                try:
                    transactions = json.loads(trans_match.group(1))
                    
                    # Extract account details
                    account_match = re.search(r'"accountDetails":\s*({[\s\S]*?})', failed_json)
                    account_details = {}
                    if account_match:
                        try:
                            account_details = json.loads(account_match.group(1))
                        except:
                            # Use regex to extract key fields
                            account_no = re.search(r'"accountNo":\s*"([^"]*)"', failed_json)
                            opening_balance = re.search(r'"openingBalance":\s*([\d\.]+)', failed_json)
                            
                            if account_no:
                                account_details["accountNo"] = account_no.group(1)
                            if opening_balance:
                                account_details["openingBalance"] = float(opening_balance.group(1))
                    
                    # Construct a clean financial data object
                    return {
                        "accountDetails": account_details,
                        "transactions": transactions
                    }
                except:
                    pass
                    
        # If all attempts to fix the JSON fail, raise an appropriate exception
        raise HTTPException(
            status_code=500,
            detail="Failed to process financial data: Could not extract valid JSON from the response"
        )
            
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")
        error_detail = str(e)
        if hasattr(e, 'response') and e.response:
            error_detail = f"{str(e)} - Response: {e.response.text}"
        raise HTTPException(status_code=500, detail=f"Groq API request failed: {error_detail}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# If you need an async version of this function for use with FastAPI
async def process_groq_data_async(input_data: dict):
    """
    Async wrapper for the Groq API service.
    """
    import asyncio
    return await asyncio.to_thread(process_groq_data, input_data)