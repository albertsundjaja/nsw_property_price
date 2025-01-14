import os
import requests
import zipfile
import pandas as pd
from pathlib import Path

def download_and_unzip():
    # Create folder raw_data if not exist
    output_dir = Path(__file__).parent / 'src' / 'assets' / 'raw_data'
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(2, 5):
        url = f"https://www.valuergeneral.nsw.gov.au/__psi/yearly/202{i}.zip"
        output_path = output_dir / f"202{i}.zip"

        # Download the zip file
        print(f"Downloading {url}...")
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch {url}: {response.status_code} {response.reason}")

        # Save the zip file
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded to {output_path}")

        # Extract the zip file
        with zipfile.ZipFile(output_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
            print(f"Extracted to {output_dir}")

        # Remove the zip file after extraction
        os.remove(output_path)
        print(f"Removed {output_path}")

# Function to process a single .DAT file and extract B records
def process_dat_file(file, zip_file, output_handle):
    try:
        with zip_file.open(file) as f:
            for line in f:
                decoded_line = line.decode('utf-8').strip()
                if decoded_line.startswith('B;'):  # Filter B records
                    output_handle.write(decoded_line + '\n')
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Function to process all zip files in a folder and extract B records
def process_zip_files(folder_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as output_handle:
        for zip_file_name in os.listdir(folder_path):
            if zip_file_name.endswith('.zip'):
                zip_file_path = os.path.join(folder_path, zip_file_name)
                try:
                    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                        dat_files = [name for name in zip_file.namelist() if name.endswith('.DAT')]
                        for dat_file in dat_files:
                            process_dat_file(dat_file, zip_file, output_handle)
                except zipfile.BadZipFile as e:
                    print(f"Error opening {zip_file_name}: {e}")
    print(f"All B records saved to {output_file}")

def process_data(file_path):
    # Process the data
    columns_b = [
        "Record Type", "District Code", "Property Id", "Sale Counter", "Download Date/Time",
        "Property Name", "Property Unit Number", "Property House Number", "Property Street Name",
        "Property Locality", "Property Post Code", "Area", "Area Type", "Contract Date",
        "Settlement Date", "Purchase Price", "Zoning", "Nature of Property", "Primary Purpose",
        "Strata Lot Number", "Component Code", "Sale Code", "% Interest of Sale", "Dealing Number"
    ]
    df = pd.read_csv(file_path, sep=';', header=None, names=columns_b, dtype='str', usecols=range(24))
    # Convert numeric columns
    df["Purchase Price"] = pd.to_numeric(df["Purchase Price"], errors='coerce')
    df["Area"] = pd.to_numeric(df["Area"], errors='coerce')
    df["% Interest of Sale"] = pd.to_numeric(df["% Interest of Sale"], errors='coerce')
    df = df.groupby('Property Locality').mean(numeric_only=True).reset_index()
    df = df.sort_values(by='Purchase Price', ascending=False)
    df = df.head(100)
    output_file = Path(__file__).parent / 'src' / 'assets' / 'raw_data'
    df.to_csv(output_file, index=False)

# Specify the folder containing zip files and the output file
folder_path = 'raw_data'
output_file = 'src/raw_assets/raw_data/combined_b_records.data'

# Run the function
if __name__ == "__main__":
    try:
        # Run the function
        download_and_unzip()
        process_zip_files(folder_path, output_file)
        process_data(output_file)
    except Exception as e:
        print(f"An error occurred: {e}")
