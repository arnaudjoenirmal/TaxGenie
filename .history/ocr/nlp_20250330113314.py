import json
import spacy
import re

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Define regex patterns for structured data
AMOUNT_PATTERN = r"(?:\₦|\$|\€)?\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
ACC_NUM_PATTERN = r"\b\d{10,12}\b"  # Capture 10-12 digit bank account numbers
SORT_CODE_PATTERN = r"\d{2}-\d{2}-\d{2}"  # Matches sort codes

# List of known banks
KNOWN_BANKS = ["Guaranty Trust", "GTBank", "Access Bank", "Zenith Bank", "First Bank"]

# Load extracted JSON file
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Extract structured values using regex
def extract_regex(text, pattern):
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""

# Extract bank name from known list
def extract_bank_name(text):
    for bank in KNOWN_BANKS:
        if bank.lower() in text.lower():
            return bank
    return ""

# Use NLP to extract and map relevant info
def extract_entities(text):
    doc = nlp(text)
    extracted_data = {
        "bank_name": extract_bank_name(text),
        "account_number": extract_regex(text, ACC_NUM_PATTERN),
        "sort_code": extract_regex(text, SORT_CODE_PATTERN),
        "reference": "",
        "opening_balance": "",
        "closing_balance": "",
        "payments_in": "",
        "payments_out": ""
    }
    
    # Extract amounts for opening & closing balances
    amounts = re.findall(AMOUNT_PATTERN, text)
    if amounts:
        extracted_data["opening_balance"] = amounts[0]
        if len(amounts) > 1:
            extracted_data["closing_balance"] = amounts[-1]
    
    return extracted_data

# Process extracted JSON
def process_extracted_json(json_data):
    full_text = json.dumps(json_data)  # Convert JSON to text
    return extract_entities(full_text)

# Example Usage
if __name__ == "__main__":
    file_path = r"D:\\TaxGenie_dataset\\5.jpg.json"  # Replace with your JSON file
    extracted_json = load_json(file_path)
    clean_data = process_extracted_json(extracted_json)
    print(json.dumps(clean_data, indent=4))
