import requests
import pandas as pd
from datetime import datetime
import math
from time import sleep

import os
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
    #convert into pandas dataframe
    entergy = pd.DataFrame(data)
    #label utility as entergy
    entergy["utility"] = "Entergy"
    #add current time to a column
    entergy["date pulled"] = date_str
    entergy["time pulled"] = time_str
    #use a single file for all results
    csv_file = f"data/{location.lower()}/{area}/entergy/all_data.csv"
    write_header = not os.path.isfile(csv_file)
    entergy.to_csv(csv_file, mode='a', header=write_header, index=False)
    return entergy
    print(path)
    entergy["percentAffected"] = entergy["customersAffected"] / entergy["customersServed"]
    entergy.to_csv(path)
    return entergy
