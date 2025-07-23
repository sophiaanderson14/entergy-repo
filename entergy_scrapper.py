import requests
import pandas as pd
from datetime import datetime
import math
from time import sleep
import os
import entergy_scrapper
import gspread
from google.oauth2.service_account import Credentials

# Import Google Sheets helper for Louisiana county data
try:
    from google_sheets_helper import append_to_google_sheet
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False
    print("Warning: Google Sheets integration not available. Install gspread and google-auth packages.")
def current_entergy(location,area):
    #opening base URL
    url = "https://entergy.datacapable.com/datacapable/v1/entergy/Entergy{}/{}".format(location,area)
    print(url)
    #get current time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M").lstrip("0").replace(" 0", " ")
    #go to webpage
    r = requests.get(url)
    #convert into json
    data = r.json()
    print(data)  # Debug: inspect API response

    if isinstance(data, dict) and 'results' in data:
        entergy = pd.DataFrame(data['results'])
    else:
        entergy = pd.DataFrame(data)
        # Ensure output directory exists
    csv_file = "data/louisiana/zip/entergy/all_data.csv"
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    # Define replace_dict before it's used
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
    if 'county' in entergy.columns:
        entergy["county"] = entergy["county"].replace(replace_dict)
    else:
        print("Warning: 'county' column not found in DataFrame.")
        entergy["county"] = ""  # or handle as needed

    if 'county' in entergy.columns:
        entergy["county"] = entergy["county"].replace(replace_dict)
    else:
        print("Warning: 'county' column not found in DataFrame.")
        entergy["county"] = ""  # or handle as needed
        #label utility as entergy
    entergy["utility"] = "Entergy"
    #add current time to a column
    entergy["date pulled"] = date_str
    entergy["time pulled"] = time_str

    # CALCULATE PERCENT WITHOUT POWER BEFORE SAVING
    if "customersAffected" in entergy.columns and "customersServed" in entergy.columns:
        entergy["percentWithoutPower"] = (entergy["customersAffected"] / entergy["customersServed"]).round(2)
    else:
        entergy["percentWithoutPower"] = None

    # Special handling for Louisiana county data - use Google Sheets
    if location.lower() == "louisiana" and area.lower() == "county":
        if GOOGLE_SHEETS_AVAILABLE:
            success = _append_to_google_sheets(entergy)
            if success:
                print("Data successfully appended to Google Sheet")
                return entergy
            else:
                print("Failed to append to Google Sheet, falling back to CSV")
        else:
            print("Google Sheets not available, using CSV fallback")
    
    # Default behavior: save to CSV file
    csv_file = f"data/{location.lower()}/{area}/entergy/all_data.csv"
    write_header = not os.path.isfile(csv_file)
    entergy.to_csv(csv_file, mode='a', header=write_header, index=False)
    return entergy


def _append_to_google_sheets(df: pd.DataFrame) -> bool:
    """
    Helper function to append data to Google Sheets for Louisiana county data.
    
    Args:
        df (pd.DataFrame): The data to append
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get Google Sheet URL from environment variable or config
        sheet_url = os.getenv("GOOGLE_SHEET_URL", "")
        
        if not sheet_url:
            print("Error: GOOGLE_SHEET_URL environment variable not set")
            return False
        
        # Try to append to Google Sheet
        return append_to_google_sheet(
            df=df,
            sheet_url=sheet_url,
            credentials_file="credentials.json",
            worksheet_name="Sheet1"
        )
        
    except Exception as e:
        print(f"Error appending to Google Sheet: {e}")
        return False
