import re
from datetime import datetime

def clean_dict_values(row_dict):
    """
    Clean the values in the dictionary, focusing on removing symbols from numbers.
    """
    for key, value in row_dict.items():
        # Directly clean numerical fields
        if key in ['Balance', 'Paid out', 'Paid in']:
            # Remove any non-digit and non-decimal characters from numbers
            cleaned_value = re.sub(r'[^\d.]+', '', value)
            try:
                row_dict[key] = str(cleaned_value)
            except ValueError:
                print(f"Error converting to float: {value}")
                row_dict[key] = None  # or keep the original value
        elif key == 'Date' and value:
            row_dict[key] = convert_date_format(value)
    return row_dict

def convert_date_format(date_string):
    """
    Converts a date from '12 Feb 2024' format to 'dd.mm.yyyy' format.
    """
    try:
        date_obj = datetime.strptime(date_string, '%d %b %Y')
        return date_obj.strftime('%d.%m.%Y')
    except ValueError:
        print(f"Error parsing date: {date_string}")
        return date_string
