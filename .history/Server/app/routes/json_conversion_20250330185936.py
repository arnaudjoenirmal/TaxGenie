import json
import re

# Parse the entire API response
response_data = json.loads(open('paste.txt').read())

# Extract the content field from the message
content_str = response_data["choices"][0]["message"]["content"]

# The content contains a JSON inside markdown code blocks
# Extract the JSON string using regex
json_match = re.search(r'```\n(.*?)\n```', content_str, re.DOTALL)

if json_match:
    json_str = json_match.group(1)
    # Parse the extracted JSON string
    extracted_data = json.loads(json_str)
    
    # Now you have just the structured data
    # Save it to a new file
    with open('extracted_data.json', 'w') as f:
        json.dump(extracted_data, f, indent=2)
    
    print("Data successfully extracted and saved to extracted_data.json")
else:
    print("Could not find JSON data in the content")