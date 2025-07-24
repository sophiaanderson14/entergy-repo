import gspread
import pandas as pd
import os

# Authenticate and connect
import json

filename = 'data.json'
if os.path.exists(filename):
    with open(filename) as f:
        content = f.read()
        if not content.strip():
            raise ValueError("JSON input is empty.")
        data = json.loads(content)
else:
    raise FileNotFoundError(f"{filename} does not exist.")
SHEET_NAME = 'Entergy'
from google.oauth2.service_account import Credentials

import sys  # add this at the top if not already present

# --- START: MODIFIED SECTION FOR GITHUB ACTIONS ---
# This block replaces the original file-based authentication.
# It reads the credentials from an environment variable.

# 1. Get the JSON string from the environment variable
creds_json_string = os.environ.get('GOOGLE_CREDS_JSON')

# 2. Check if the environment variable is set
if not creds_json_string:
    print("Error: The GOOGLE_CREDS_JSON environment variable is not set.")
    sys.exit(1)

try:
    # 3. Load the JSON string into a Python dictionary
    creds_dict = json.loads(creds_json_string)
    
    # 4. Authorize gspread using the credentials dictionary
    gc = gspread.service_account_from_dict(creds_dict)

except json.JSONDecodeError:
    print("Error: Could not decode the GOOGLE_CREDS_JSON. Ensure it's a valid, single-line JSON in your GitHub Secret.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred during gspread authorization: {e}")
    sys.exit(1)
# --- END: MODIFIED SECTION FOR GITHUB ACTIONS ---


sheet = gc.open(SHEET_NAME).sheet1

import pandas as pd

def current_entergy(state, granularity):
    """
    Fetches current Entergy data for a given state and granularity (e.g., 'county' or 'zip').
    Returns a pandas DataFrame with the results.
    Replace the logic below with your actual data retrieval logic.
    """
    # Example mock data
    if granularity == "county":
        data = {
            "county": ["ACADIA", "ALLEN"],
            "longitude": [-92.52246006, -92.68816176]
        }
    elif granularity == "zip":
        data = {
            "zip": ["70112", "70113"],
            "value": [50, 70]
        }
    else:
        data = {}

    return pd.DataFrame(data)

# Fetch data
data = entergy_scrapper.current_entergy("Louisiana", "county")  # or your API call

# County renaming logic
replace_dict = {
    "E. BATON ROUGE": "EAST BATON ROUGE",
    "W. BATON ROUGE": "WEST BATON ROUGE",
    "E. CARROLL": "EAST CARROLL",
    "W. CARROLL": "WEST CARROLL",
    "E. FELICIANA": "EAST FELICIANA",
    "W. FELICIANA": "WEST FELICIANA",
    "LA SALLE": "LASALLE",
    # Add any other replacements here
}
if 'county' in data.columns:
    data['county'] = data['county'].replace(replace_dict)
else:
    print("Warning: 'county' column not found in DataFrame.")
    data['county'] = ""

# Convert DataFrame to list of lists (including header)
sheet_data = [data.columns.tolist()] + data.astype(str).values.tolist()

# Clear the sheet and batch update
sheet.clear()
sheet.update('A1', sheet_data)
