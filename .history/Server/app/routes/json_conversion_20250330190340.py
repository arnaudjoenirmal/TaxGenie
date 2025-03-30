import json
import re

# Load API response JSON from file
with open('paste.txt', 'r', encoding='utf-8') as f:
    response_data = json.load(f)  # Directly parse JSON

# Extract the message content
content_str = response_data["choices"][0]["message"]["content"]

# Remove markdown triple backticks and extract JSON
json_match = re.search(r'```json\n(.*?)\n```', content_str, re.DOTALL)

if json_match:
    json_str = json_match.group(1)  # Extract JSON as string
    extracted_data = json.loads(json_str)  # Parse JSON

    # Save cleaned JSON to file
    with open('extracted_data.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=2)

    print("✅ Data successfully extracted and saved to extracted_data.json")
else:
    print("❌ Could not find JSON data in the content")
