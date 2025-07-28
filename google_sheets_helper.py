import gspread
from google.auth.exceptions import GoogleAuthError
import pandas as pd
import os
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleSheetsHelper:
    """Helper class for Google Sheets operations."""
    
    def __init__(self, credentials_file: str = "credentials.json"):
        """
        Initialize the Google Sheets helper.
        
        Args:
            credentials_file (str): Path to the Google service account credentials JSON file
        """
        self.credentials_file = credentials_file
        self.client = None
        self.sheet = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with Google Sheets API using service account credentials.
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            if not os.path.exists(self.credentials_file):
                logger.error(f"Credentials file not found: {self.credentials_file}")
                return False
            
            self.client = gspread.service_account(filename=self.credentials_file)
            logger.info("Successfully authenticated with Google Sheets API")
            return True
            
        except GoogleAuthError as e:
            logger.error(f"Google authentication error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during authentication: {e}")
            return False
    
    def open_sheet(self, sheet_url: str, worksheet_name: str = "Entergy") -> bool:
        """
        Open a Google Sheet by URL.
        
        Args:
            sheet_url (str): The Google Sheet URL or key
            worksheet_name (str): Name of the worksheet (default: "Entergy")
            
        Returns:
            bool: True if sheet opened successfully, False otherwise
        """
        try:
            if not self.client:
                logger.error("Not authenticated. Please call authenticate() first.")
                return False
            
            # Extract sheet key from URL if a full URL is provided
            if "docs.google.com/spreadsheets" in sheet_url:
                sheet_key = sheet_url.split("/d/")[1].split("/")[0]
            else:
                sheet_key = sheet_url
            
            spreadsheet = self.client.open_by_key(sheet_key)
            self.sheet = spreadsheet.worksheet(worksheet_name)
            logger.info(f"Successfully opened sheet: {spreadsheet.title}")
            return True
            
        except gspread.exceptions.SpreadsheetNotFound:
            logger.error(f"Spreadsheet not found or not accessible: {sheet_url}")
            return False
        except gspread.exceptions.WorksheetNotFound:
            logger.error(f"Worksheet '{worksheet_name}' not found")
            return False
        except Exception as e:
            logger.error(f"Error opening sheet: {e}")
            return False
    
    def append_dataframe(self, df: pd.DataFrame, include_headers: bool = None) -> bool:
        """
        Append a pandas DataFrame to the Google Sheet.
        
        Args:
            df (pd.DataFrame): The DataFrame to append
            include_headers (bool): Whether to include headers. If None, auto-detect based on sheet content
            
        Returns:
            bool: True if data appended successfully, False otherwise
        """
        try:
            if not self.sheet:
                logger.error("No sheet opened. Please call open_sheet() first.")
                return False
            
            if df.empty:
                logger.warning("DataFrame is empty, nothing to append")
                return True
            
            # Convert DataFrame to list of lists
            values = df.values.tolist()
            
            # Determine if we need to include headers
            if include_headers is None:
                # Auto-detect: include headers if sheet is empty
                existing_data = self.sheet.get_all_values()
                include_headers = len(existing_data) == 0
            
            if include_headers:
                # Prepend headers
                headers = df.columns.tolist()
                values.insert(0, headers)
            
            # Append the data
            self.sheet.append_rows(values)
            logger.info(f"Successfully appended {len(df)} rows to the sheet")
            return True
            
        except Exception as e:
            logger.error(f"Error appending data to sheet: {e}")
            return False
    
    def get_sheet_url(self) -> Optional[str]:
        """
        Get the URL of the currently opened sheet.
        
        Returns:
            str: The sheet URL, or None if no sheet is opened
        """
        if self.sheet:
            return f"https://docs.google.com/spreadsheets/d/{self.sheet.spreadsheet.id}"
        return None


def append_to_google_sheet(df: pd.DataFrame, 
                          sheet_url: str = None, 
                          credentials_file: str = "credentials.json",
                          worksheet_name: str = "Entergy") -> bool:
    """
    Convenience function to append data to a Google Sheet.
    If sheet_url is not provided, tries to use the GOOGLE_SHEET_URL environment variable.
    
    Args:
        df (pd.DataFrame): The DataFrame to append
        sheet_url (str): The Google Sheet URL or key (optional)
        credentials_file (str): Path to the credentials file
        worksheet_name (str): Name of the worksheet
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not sheet_url:
        sheet_url = os.getenv("GOOGLE_SHEET_URL")
        if not sheet_url:
            logger.error("Google Sheet URL not provided and GOOGLE_SHEET_URL environment variable not set.")
            return False

    helper = GoogleSheetsHelper(credentials_file)
    
    if not helper.authenticate():
        return False
    
    if not helper.open_sheet(sheet_url, worksheet_name):
        return False
    
    return helper.append_dataframe(df)
