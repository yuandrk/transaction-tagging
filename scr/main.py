import os
import sys
from csv_processing import process_csv
from utils import generate_output_filename

if __name__ == "__main__":
    # Define the directory where CSV files are stored
    data_directory = "./data"
    
    # Check if the data directory exists
    if not os.path.exists(data_directory):
        print(f"The directory {data_directory} does not exist.")
        sys.exit(1)
    
    # Retrieve a list of CSV files in the data directory
    csv_files = [file for file in os.listdir(data_directory) if file.endswith('.csv')]
    
    # Check if there are CSV files in the directory
    if not csv_files:
        print(f"No CSV files found in the directory {data_directory}.")
        sys.exit(1)

    # Process each CSV file
    for file_name in csv_files:
        file_path = os.path.join(data_directory, file_name)
        output_file_name = generate_output_filename() 
        process_csv(file_path, output_file_name)
        print(f"Processed {file_path} and generated {output_file_name}")
