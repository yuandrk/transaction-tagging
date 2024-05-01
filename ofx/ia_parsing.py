from openai import OpenAI 

client = OpenAI()

def create_category(payee):
    """
    Generates tags for a transaction based on its type and paid out value using OpenAI's GPT.

    :param transaction_type: The type of the transaction (e.g., 'Groceries', 'Utilities').
    :param paid_out: The amount paid out for the transaction.
    :return: Generated tags as a string.
    """
    # Preparing the message for the OpenAI API
    response = client.chat.completions.create(
         messages = [
               {"role": "system", "content": "You are a helpful assistant."},
               {"role": "user", "content": f"""
               Based on the description '{payee}', provide a single-word tag. 
               The tag should be a relevant keyword, typical for categories like shopping, grocery, travel, etc., without any additional symbols.
               """}
            ],
         model="gpt-3.5-turbo-1106",
         max_tokens=64,
         temperature=0
      )
    
    return response.choices[0].message.content.strip()

