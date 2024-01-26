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
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Based on the description '{description}', provide a single-word tag. The tag should be a relevant keyword, typical for categories like shopping, grocery, travel, etc., without any additional symbols."}
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
