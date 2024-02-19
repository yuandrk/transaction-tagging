import csv
import sys
from pprint import pprint


file = sys.argv[1]

def read_csv_to_dicts(file):
    """
    Reads a CSV file and returns a list of dictionaries.
    Each dictionary represents a row from the file, with keys corresponding to the column headers.
    
    :param filename: The path to the CSV file to be read.
    :return: A list of dictionaries, where each dictionary represents a row from the CSV file.
    """
    data = []  
    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:    
            data.append(row)
    return data

rows_as_dicts = read_csv_to_dicts(file)

pprint(rows_as_dicts[2])


def clean_dict_values(row_dict):
    """
    Clean the values in the dictionary.
    """
    for key, value in row_dict.items():
        # Remove currency symbol and convert to float, if applicable
        if key in ['Balance', 'Paid out'] and value.startswith('�'):
           row_dict[key] = float(value.replace('�', ''))
        # Add more cleaning rules as needed
        #### start work here ####
    return row_dict

# Clean a specific row from the CSV
clean_dict = clean_dict_values(rows_as_dicts[2])
pprint(clean_dict)