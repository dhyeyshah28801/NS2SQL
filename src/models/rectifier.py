import openai
import json 

def rectify_statement(schema, recorded_statement):
    openai.api_key = "DEMO_API_KEY"  # Replace with your OpenAI API key

    # Prepare the prompt for OpenAI ChatGPT
    prompt = (
        "You are a helpful assistant skilled in databases and language processing. "
        "Here is the database schema: "
        f"{json.dumps(schema, indent=2)} "
        "Now, rectify and enhance the following statement based on the schema: "
        f"'{recorded_statement}' "
        "Return the rectified and enhanced statement as a JSON."
    )

    print('Prompt: ', prompt)
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150,
            temperature=0.5
        )
        # Parse the response
        rectified_statement = response.choices[0].text.strip()
        return rectified_statement
    except Exception as e:
        print(f"Error communicating with OpenAI API: {e}")
        return None
