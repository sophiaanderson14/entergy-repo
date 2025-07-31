# Entergy Outage Data Scraper

This repository was made to add scraped data from Entergy's power outage website to a map that can be filtered by time period. This way, users can see a snapshot of outages for any ten minute interval. This is part of a project for WWNO in New Orleans, LA in partnership with the Reynolds Journalism Institute at the University of Missouri. 

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

First, make sure the name of your Google Sheet is consistent throughout all your scripts. In order to link to a Google Sheet, you have to set up a Google Cloud authorization key. 

You can do this for free by setting up a Google Cloud account. I don’t recommend doing this from a Google account linked to your company or university because your account may have built in restrictions that limit this part of the process. You can set up a Google Cloud account from any email address. Note that if you have trouble finding any of the settings mentioned in the following steps, you can always search for them within Google Cloud. 

Go to https://console.cloud.google.com/ 
Create a new project by clicking on IAM & Admin. You can also search for Create a Project

Once you’ve created and named your project, go to APIs and services and then Library. Search for Google Sheets API. Click on it and choose Enable
Go to APIs and Services then Credentials. Choose Create Credentials and choose Service account. The only information you need to add is the name, everything else is optional. 
Go to te Keys tab, choose Create new key and choose the JSON format. The key will download. Name it “credentials” and save it to the same folder on your computer as the rest of the files in your repository. Do not upload it to your repository. 
Share your Google Sheet with the email in your credentials JSON (give edit access). To find the email, open the JSON in Notepad or a similar app on your computer. 

Now you’ll create a GitHub secret to store the information on your credentials JSON. This is more secure than uploading the JSON to your repository. 

In your repository, go to Settings, Secrets and Variables, then Actions
Under Repository secrets, choose Create a new secret  
Copy and paste the full contents of your credentials JSON into the secret and save it

Note: Sometimes copying and pasting a file like this will add extra spaces or characters that you can’t see and cause your code to fail. I solved this issue by converting the JSON into one line using this converter. I copied and pasted the converted one-line JSON into the secret.

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
