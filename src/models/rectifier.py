from openai import OpenAI
import json 
#from dotenv import load_dotenv
import os
#load_dotenv()

def rectify_statement(schema, recorded_statement):
    client = OpenAI(api_key="API_KEY")

    # Prepare the prompt for OpenAI ChatGPT
    prompt = (
        "Here is the database schema: "
        f"{json.dumps(schema, indent=2)} "
        "Now, rectify and enhance the following statement based on the schema: "
        f"'{recorded_statement}' "
        "Use the rectified and enhanced statement and convert it to an SQL query."
        "Only Return the SQL query in a json stringified format and do not return an extra letter."
    )

    #print('Prompt: ', prompt)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in databases and language processing.."},
                {"role": "user", "content": prompt}
            ]
        )
        print(completion.choices[0].message.content)
        # Parse the response
        rectified_statement = completion.choices[0].message.content
        return rectified_statement
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return None
