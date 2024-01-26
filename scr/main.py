import sys
from csv_processing import process_csv
from utils import generate_output_filename

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        output_file_name = generate_output_filename()
        process_csv(file_path, output_file_name)