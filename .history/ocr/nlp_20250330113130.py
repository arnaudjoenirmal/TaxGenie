import json
import spacy
import re

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Define regex patterns for structured data
AMOUNT_PATTERN = r"(?:€|\$)?\s?\d{1,3}(?:,\d{3})*(?:\.\d+)?"
DATE_PATTERN = r"\d{1,2}[a-z]{2}\s[A-Za-z]+\s\d{4}"
ACC_NUM_PATTERN = r"\d{6,}"  # Matches account numbers
SORT_CODE_PATTERN = r"\d{2}-\d{2}-\d{2}"  # Matches sort codes

# Load extracted JSON file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Extract structured values using regex
def extract_regex(text, pattern):
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""

# Use NLP to extract and map relevant info
def extract_entities(text):
    doc = nlp(text)
    extracted_data = {
        "bank_name": "",
        "account_number": "",
        "sort_code": "",
        "reference": "",
        "opening_balance": "",
        "closing_balance": "",
        "payments_in": "",
        "payments_out": "",
    }
    
    # Extract key info using NLP
    for ent in doc.ents:
        if ent.label_ == "ORG" and not extracted_data["bank_name"]:
            extracted_data["bank_name"] = ent.text
        elif ent.label_ == "MONEY":
            if not extracted_data["opening_balance"]:
                extracted_data["opening_balance"] = ent.text
            else:
                extracted_data["closing_balance"] = ent.text
        elif ent.label_ == "CARDINAL":
            if not extracted_data["account_number"]:
                extracted_data["account_number"] = ent.text
        
    # Extract structured values with regex
    extracted_data["account_number"] = extract_regex(text, ACC_NUM_PATTERN)
    extracted_data["sort_code"] = extract_regex(text, SORT_CODE_PATTERN)
    extracted_data["opening_balance"] = extract_regex(text, AMOUNT_PATTERN)
    extracted_data["closing_balance"] = extract_regex(text, AMOUNT_PATTERN)
    
    return extracted_data

# Process extracted JSON
def process_extracted_json(json_data):
    full_text = json.dumps(json_data)  # Convert JSON to text
    return extract_entities(full_text)

# Example Usage
if __name__ == "__main__":
    file_path = r"D:\TaxGenie_dataset\5.jpg.json"  # Replace with your JSON file
    extracted_json = load_json(file_path)
    clean_data = process_extracted_json(extracted_json)
    print(json.dumps(clean_data, indent=4))
