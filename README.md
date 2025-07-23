# Entergy Outage Data Scraper

This repository contains scripts to scrape power outage data from Entergy's API and store it in CSV files or Google Sheets.

## Features

- Scrapes outage data for Louisiana and Mississippi (both county and zip level)
- Automatically calculates percentage without power
- **Google Sheets Integration**: Louisiana county data is automatically appended to a public Google Sheet
- CSV fallback for all other locations and areas

## Setup

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sophiaanderson14/entergy-repo.git
cd entergy-repo
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Google Sheets Setup (for Louisiana County Data)

For Louisiana county data to be automatically saved to Google Sheets instead of CSV, follow these steps:

#### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click on it and press "Enable"

#### 2. Create Service Account Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details and click "Create"
4. On the permissions page, you can skip adding roles (click "Continue")
5. Click "Done"
6. Click on the created service account
7. Go to the "Keys" tab
8. Click "Add Key" > "Create New Key"
9. Choose "JSON" format and click "Create"
10. Save the downloaded JSON file as `credentials.json` in the project root directory

#### 3. Create and Configure Google Sheet

1. Create a new Google Sheet at [sheets.google.com](https://sheets.google.com)
2. Copy the sheet URL (should look like: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`)
3. Share the sheet with your service account:
   - Click "Share" in the top right
   - Add the service account email (found in the `credentials.json` file under `client_email`)
   - Give it "Editor" permissions
4. Make the sheet publicly viewable:
   - Click "Share" > "Change to anyone with the link"
   - Set permission to "Viewer"
   - Copy the sharing link

#### 4. Set Environment Variable

Set the Google Sheet URL as an environment variable:

**Linux/Mac:**
```bash
export GOOGLE_SHEET_URL="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"
```

**Windows:**
```cmd
set GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID
```

Or add it to your system environment variables permanently.

## Usage

### Running the Scraper

To run the complete scraping process:

```bash
python main.py
```

This will:
- Scrape Louisiana zip data → Save to CSV
- **Scrape Louisiana county data → Save to Google Sheet** (if configured)
- Scrape Mississippi county data → Save to CSV  
- Scrape Mississippi zip data → Save to CSV

### Running Individual Scrapers

You can also run individual scrapers:

```python
import entergy_scrapper

# Scrape specific location and area
entergy_scrapper.current_entergy("Louisiana", "county")  # → Google Sheet
entergy_scrapper.current_entergy("Louisiana", "zip")     # → CSV
entergy_scrapper.current_entergy("Mississippi", "county") # → CSV
```

## Data Format

The scraped data includes the following columns:

- `state`: State abbreviation (L for Louisiana, M for Mississippi)
- `county`: County name
- `customersServed`: Total customers in the area
- `customersAffected`: Customers currently without power
- `percentageWithPower`: Percentage of customers with power
- `lastUpdatedTime`: Timestamp from the API
- `latitude`: Geographic latitude
- `longitude`: Geographic longitude
- `utility`: Always "Entergy"
- `date`: Date when data was pulled (YYYY-MM-DD)
- `time`: Time when data was pulled (H:MM format)
- `percentWithoutPower`: Calculated percentage without power (customersAffected/customersServed)

## File Structure

```
entergy-repo/
├── entergy_scrapper.py      # Main scraping logic
├── google_sheets_helper.py  # Google Sheets integration
├── main.py                  # Main execution script
├── requirements.txt         # Python dependencies
├── credentials.json         # Google service account credentials (not in repo)
├── data/                    # CSV output directory
│   ├── louisiana/
│   │   ├── county/entergy/  # Louisiana county CSVs (fallback only)
│   │   └── zip/entergy/     # Louisiana zip CSVs
│   └── mississippi/
│       ├── county/entergy/  # Mississippi county CSVs
│       └── zip/entergy/     # Mississippi zip CSVs
└── README.md               # This file
```

## Troubleshooting

### Google Sheets Issues

**"Credentials file not found"**: Make sure `credentials.json` is in the project root directory and contains valid service account credentials.

**"Spreadsheet not found or not accessible"**: Ensure the service account email has been given Editor access to the Google Sheet.

**"GOOGLE_SHEET_URL environment variable not set"**: Set the environment variable with your Google Sheet URL.

**Falls back to CSV**: If Google Sheets integration fails, the scraper will automatically fall back to saving Louisiana county data in CSV format.

### API Issues

**Connection errors**: The Entergy API may be temporarily unavailable. The script will show the attempted URL for debugging.

**Data format changes**: If the API response format changes, you may need to update the column handling in `entergy_scrapper.py`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Notes

- The `credentials.json` file is automatically excluded from git via `.gitignore`
- Google Sheets integration is only used for Louisiana county data
- All other combinations (Louisiana zip, Mississippi county/zip) continue to use CSV files
- The Google Sheet should be manually shared for public viewing after setup