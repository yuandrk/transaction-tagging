import csv
from data_cleaning import clean_data

def process_csv(file_path, output_file_name):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = [clean_data(row) for row in reader]

        with open(output_file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        print(f"Output file generated: {output_file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")
