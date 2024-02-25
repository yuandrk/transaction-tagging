import sys
from csv_reader import read_csv_to_dicts
from data_cleaner import clean_dict_values
from tagging_ia import generate_transaction_tags
from pprint import pprint 
csv_file_path = sys.argv[1]

# Define the main function that orchestrates the workflow
def main():
    # Read the CSV data into a list of dictionaries
    data_dicts = read_csv_to_dicts(csv_file_path)
    # Clean the data
    cleaned_data = [clean_dict_values(data_dict) for data_dict in data_dicts]
    # Initialize tagging_data list to store tagging results
    tagging_data = []
    # Iterate over cleaned_data to apply tagging
    for data_dict in cleaned_data:
        # Ensure you have 'Transaction type' and 'Paid out' keys in your data_dict
        if 'Transaction type' in data_dict and 'Paid out' in data_dict:
            tag = generate_transaction_tags(data_dict['Transaction type'], data_dict['Paid out'])
            tagging_data.append(tag)
    # Print the cleaned data
    pprint(cleaned_data)
    # Print the tagging data
    pprint(tagging_data)

    
# Check if this script is run as the main program
if __name__ == "__main__":
    main()
