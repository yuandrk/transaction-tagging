import re
from openai_integration import generate_tags
from utils import is_date
from dateutil.parser import parse

def clean_data(row):
    cleaned_row = []
    for item in row:
        if is_date(item):
            try:
                parsed_date = parse(item, fuzzy=True)
                item = parsed_date.strftime("%d.%m.%Y")
            except ValueError:
                pass
        else:
            item = re.sub(r'[^\w\s.,]', '', item)
            if item.replace('.', '', 1).replace(',', '').isdigit():
                item = item.replace('.', ',')
        cleaned_row.append(item)
    
    # Generate tags using OpenAI API (assuming description is in the first column)
    tag = generate_tags(cleaned_row[0])
    cleaned_row.append(tag)

    return cleaned_row
