from openai import OpenAI
import json 
#from dotenv import load_dotenv
import os
#load_dotenv()

def rectify_statement(schema, recorded_statement):
    client = OpenAI(api_key="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")

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
        # Parse the response
        rectified_statement = completion.choices[0].message.content
        return rectified_statement
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return None
