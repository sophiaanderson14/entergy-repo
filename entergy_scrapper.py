import entergy_scrapper
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
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
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)
sheet = gc.open(SHEET_NAME).sheet1

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
