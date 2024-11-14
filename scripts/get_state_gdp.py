import requests
import zipfile
import os
import pandas as pd

# Step 1: Download the ZIP file
url = "https://apps.bea.gov/regional/zip/SAGDP.zip"
zip_file_path = "SAGDP.zip"

response = requests.get(url)
with open(zip_file_path, 'wb') as file:
    file.write(response.content)

# Step 2: Unzip the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall("../datasets/SAGDP_data")

# Step 3: Summarize data from each CSV file
summary_data = []

# List of valid state abbreviations
valid_states = {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
                'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'}

# Loop through each CSV file in the extracted folder
for filename in os.listdir("../datasets/SAGDP_data"):
    if filename.endswith(".csv"):
        # Split the filename and check if the last part is a valid state
        filename_split = filename.split('_')
        type = filename_split[0]
        state = filename_split[1]
        print(type)
        if state in valid_states and type == "SAGDP2N":  # Check if the last part is a valid state abbreviation
            file_path = os.path.join("../datasets/SAGDP_data", filename)
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Filter for rows where LineCode is 1
            df = df[df['LineCode'] == 1.0]  # Add this line to filter
            print(df.head())
            
            # Filter for years 2000 to 2023
            df_filtered = df.loc[:, ['GeoFIPS', 'GeoName', 'Unit'] + [str(year) for year in range(2000, 2024)]]
            
            # Summarize the data (e.g., sum or mean)
            summary = df_filtered.sum(numeric_only=True)
            
            # Add the state information to the summary
            summary['GeoFIPS'] = df_filtered['GeoFIPS'].iloc[0]  # Add GeoFIPS
            summary['GeoName'] = df_filtered['GeoName'].iloc[0]  # Add GeoName
            summary['Unit'] = df_filtered['Unit'].iloc[0]  # Add Unit
            summary['State'] = state  # Add State Acronym
            summary_data.append(summary)

# Step 4: Create a DataFrame from the summary data
summary_df = pd.DataFrame(summary_data)

# Step 5: Save the combined summary data to a single CSV file
summary_df.to_csv("../datasets/combined_summary_2000_2023.csv", index=False)

print("Data summarization complete. Combined summary file saved as 'combined_summary_2000_2023.csv'.")
