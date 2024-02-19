import re
from openai_integration import generate_tags
from utils import is_date
from dateutil.parser import parse

def extract_date(text):
    """
    Extracts the date from the text.
    """
   