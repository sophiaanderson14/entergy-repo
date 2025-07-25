import requests
import pandas as pd
from datetime import datetime
import os
import sys
import json
import gspread
from google.oauth2.service_account import Credentials

filename = 'data.json'
if os.path.exists(filename):
    with open(filename) as f:
        content = f.read()
        if not content.strip():
            raise ValueError("JSON input is empty.")
        data_json = json.loads(content)
else:
    raise FileNotFoundError(f"{filename} does not exist.")
SHEET_NAME = 'Entergy'

# Google Sheets setup (unchanged)
creds_json_string = os.environ.get('GOOGLE_CREDS_JSON')
if not creds_json_string:
    print("Error: The GOOGLE_CREDS_JSON environment variable is not set.")
    sys.exit(1)
try:
    creds_dict = json.loads(creds_json_string)
    gc = gspread.service_account_from_dict(creds_dict)
except json.JSONDecodeError:
    print("Error: Could not decode the GOOGLE_CREDS_JSON. Ensure it's a valid, single-line JSON in your GitHub Secret.")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred during gspread authorization: {e}")
    sys.exit(1)


# --- This is your web-scraping code, now integrated ---
def current_entergy(location, area):
    url = f"https://entergy.datacapable.com/datacapable/v1/entergy/Entergy{location}/{area}"
    print(url)
    now = datetime.now()
    r = requests.get(url)
    data = r.json()
    entergy = pd.DataFrame(data)
    entergy["utility"] = "Entergy"
    entergy["time pulled"] = now
    # Optionally save to CSV (as your original code does), or skip this step
    # title = f"{now.year}-{now.month}-{now.day} {now.hour}.{now.minute}"
    # path = f"data/{location.lower()}/{area}/entergy/{title}.csv"
    # entergy.to_csv(path)
    return entergy

# Use the scraper to get data
data = current_entergy("Louisiana", "county")  

data["percent without power"] = (100 * data["customersAffected"] / data["customersServed"]).round(2)

# If not already done:
data["time pulled"] = pd.to_datetime(data["time pulled"])

# Format without seconds:
data["time pulled"] = data["time pulled"].dt.strftime("%Y-%m-%d %H:%M")


# County renaming logic (unchanged)
replace_dict = {
    "E. BATON ROUGE": "EAST BATON ROUGE",
    "W. BATON ROUGE": "WEST BATON ROUGE",
    "E. CARROLL": "EAST CARROLL",
    "W. CARROLL": "WEST CARROLL",
    "E. FELICIANA": "EAST FELICIANA",
    "W. FELICIANA": "WEST FELICIANA",
    "LA SALLE": "LASALLE",
}
if 'county' in data.columns:
    data['county'] = data['county'].replace(replace_dict)
else:
    print("Warning: 'county' column not found in DataFrame.")
    data['county'] = ""

# Convert DataFrame to list of lists (including header)
sheet_data = [data.columns.tolist()] + data.astype(str).values.tolist()

# Get only the data rows (excluding header)
data_rows = data.astype(str).values.tolist()

# Open the spreadsheet
sh = gc.open(SHEET_NAME)
base_sheet_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
# Create a new worksheet/tab for this run
sheet_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
existing_sheets = [ws.title for ws in sh.worksheets()]
sheet_name = base_sheet_name

if sheet_name in existing_sheets:
    # Add seconds for uniqueness
    sheet_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    counter = 1
    orig_sheet_name = sheet_name
    while sheet_name in existing_sheets:
        sheet_name = f"{orig_sheet_name}-{counter}"
        counter += 1
worksheet = sh.add_worksheet(title=sheet_name, rows=str(len(data)+1), cols=str(len(data.columns)))
worksheet.append_row(data.columns.tolist())
worksheet.append_rows(data.astype(str).values.tolist())
