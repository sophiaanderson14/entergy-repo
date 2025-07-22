import pandas as pd

# Load the CSV file
df = pd.read_csv("data/louisiana/county/entergy/all_data.csv")

# Add the new column
df["percentWithoutPower"] = df["customersAffected"] / df["customersServed"]

# Save the updated CSV
df.to_csv("data/louisiana/county/entergy/all_data.csv", index=False)
