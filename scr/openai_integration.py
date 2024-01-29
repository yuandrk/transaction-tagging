from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_tags(description):
    try:
        print("Generating tags for:", description)  # Debug print

# Preparing the message for the OpenAI API
        messages = [
            {"role": "system", "content": "You are a smart assistant capable of understanding shopping contexts and categorizing them into specific tags."},
            {"role": "user", "content": f"Analyze the following description and categorize it into a specific tag. The tag should be a single, relevant keyword. Consider brand names like 'Tesco' or 'Lidl' as indicative of the 'grocery' category. Factor in the context of the description, which may include details about costs or shopping items. Avoid any additional symbols or text. Description: '{description}'"}
        ]

        # Making the API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            temperature=0
        )

        # Accessing the response correctly
        response_message = response.choices[0].message.content.strip()
        # Ensure the response is a single word without additional symbols
        tag = ''.join(filter(str.isalnum, response_message.split()[0]))
        print("Tag generated:", tag)  # Debug print 

        return tag
    except Exception as e:
        print(f"Error generating tags: {e}")
        return "N/A"
