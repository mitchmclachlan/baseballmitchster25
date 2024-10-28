import os
import pandas as pd

# Define the base directory where processed data is stored
PROCESSED_DIR = os.path.expanduser('~/Development/repos/baseballmitchster25/data/processed')

# Initialize an empty list to collect DataFrames
dataframes = []

# Step 1: Find all processed hitting files from 2021 onward
files = [f for f in os.listdir(PROCESSED_DIR) if 'hitting' in f.lower()]

for file in files:
    parts = file.split('_')
    season = int(parts[1])
    
    # Only consider files for 2021 forward
    if season >= 2021:
        file_path = os.path.join(PROCESSED_DIR, file)
        
        # Load the CSV into a DataFrame
        df = pd.read_csv(file_path)
        
        # Step 2: Rename 'hits' column to 'h' if it exists
        if 'hits' in df.columns:
            df = df.rename(columns={'hits': 'h'})
        
        # Step 3: Append the DataFrame to the list
        dataframes.append(df)

# Step 4: Concatenate all DataFrames, keeping all columns (even if they don't appear in all datasets)
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new CSV file
output_path = os.path.join(PROCESSED_DIR, 'combined_hitting_data_2021_onwards.csv')
combined_df.to_csv(output_path, index=False)

print(f"Combined hitting data saved to {output_path}")
