import csv

def read_csv_to_dicts(file_path):
    """
    Reads a CSV file and returns a list of dictionaries.
    Each dictionary represents a row from the file, with keys corresponding to the column headers.
    
    :param filename: The path to the CSV file to be read.
    :return: A list of dictionaries, where each dictionary represents a row from the CSV file.
    """
    data = []  
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:    
            data.append(row)
    return data

