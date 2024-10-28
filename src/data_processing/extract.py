import os
import pandas as pd
import argparse

# Define the base directory where raw data is stored
BASE_DIR = os.path.expanduser('~/Development/repos/baseballmitchster25/data/raw/bp')

# Define the output directory for processed data
PROCESSED_DIR = os.path.expanduser('~/Development/repos/baseballmitchster25/data/processed')

# Create the output directory if it doesn't exist
os.makedirs(PROCESSED_DIR, exist_ok=True)

def extract_files(force_reprocess=False):
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Handle Excel files based on their structure
            if file.endswith('.xlsx') or file.endswith('.xls'):
                if 'hitting' in file.lower():
                    category = 'hitting'
                elif 'pitching' in file.lower():
                    category = 'pitching'
                else:
                    continue

                # Extract season information from the filename
                try:
                    # Adjust the way we extract the season to match different formats
                    season = int(''.join(filter(str.isdigit, file.split('_')[0])))
                except (IndexError, ValueError) as e:
                    print(f"Skipping file with unexpected format: {file}, Error: {e}")
                    continue

                # Check if any files for the given category and season already exist
                if not force_reprocess and any(f.startswith(f"{category}_{season}") for f in os.listdir(PROCESSED_DIR)):
                    print(f"Skipping already processed file: {file} (Category: {category}, Season: {season})")
                    continue

                # Load the Excel file and process all sheets
                try:
                    excel_data = pd.ExcelFile(file_path)
                    for sheet_name in excel_data.sheet_names:
                        output_file_name = f"{category}_{season}_{sheet_name}.csv"
                        output_path = os.path.join(PROCESSED_DIR, output_file_name)

                        # Skip processing if the output file already exists
                        if not force_reprocess and os.path.exists(output_path):
                            print(f"Skipping already processed sheet: {file} (Sheet: {sheet_name})")
                            continue

                        df = pd.read_excel(excel_data, sheet_name=sheet_name)
                        df['season'] = season
                        df['percentile'] = sheet_name

                        # Save the processed DataFrame to CSV in the processed directory
                        df.to_csv(output_path, index=False)
                        print(f"Processed and saved: {output_file_name}")
                except Exception as e:
                    print(f"Error processing file {file}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract and process Excel files.")
    parser.add_argument('--force', action='store_true', help="Force reprocess all files, even if already processed.")
    args = parser.parse_args()

    extract_files(force_reprocess=args.force)
