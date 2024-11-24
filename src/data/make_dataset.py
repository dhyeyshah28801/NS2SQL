import json

# Define the file name

def fetchDatabaseSchema(filePath):
    try:
        # Open the JSON file and load it into a dictionary

        json_file = open( filePath, 'r')
        db_schema = json.load(json_file)

        # Print the dictionary
        print("Database schema as a dictionary:", db_schema)

        return db_schema

    except FileNotFoundError:
        print(f"Error: The file '{ filePath }' does not exist.")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON. Details: {e}")
