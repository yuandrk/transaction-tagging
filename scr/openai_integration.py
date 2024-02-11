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
    {
        "role": "system", 
        "content": """
            As a highly intelligent assistant, your task is to analyze detailed shopping descriptions and categorize them into specific, 
            relevant tags using only single keywords. Follow these guidelines to ensure a wide range of tags:
            - Identify the main item or service being described and use that as the basis for the tag. For example, 
            if the description is about purchasing a book, the tag should be 'Books'.
            - For grocery items or purchases from known supermarkets, consider the primary 
            type of item (e.g., 'Fruits', 'Vegetables', 'Beverages').
            - For online purchases, try to determine the type of product or service rather than 
            just tagging everything as 'Online'. For instance, 'Electronics' for gadgets, 'Apparel' for clothing bought online, etc.
            - When a brand is mentioned, use the product category associated with that brand. 
            For example, 'Adidas' or 'Nike' should lead to 'Sportswear', not just 'Clothes'.
            - Use specific tags for services (e.g., 'Streaming' for Netflix, 'Delivery' for UberEats).
            - If the description involves a payment for a utility or service, 
            categorize it by the type of service (e.g., 'Electricity', 'Internet').
            Your response should be a single, specific, and relevant keyword that best categorizes each shopping description. 
            Avoid general tags unless absolutely necessary, and do not include any additional symbols or text.
        """
    },
    {
        "role": "user", 
        "content": f"Analyze the following shopping description and suggest the most appropriate, specific tag: '{description}'"
    }
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
