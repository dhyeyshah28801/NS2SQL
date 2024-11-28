from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
 
# Load the fine-tuned model
tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-wikiSQL")
model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-wikiSQL")
 
# Function to parse the schema and extract table/column info
def parse_schema(schema):
    schema_info = {}
    try:
        schema = schema.strip().replace("Table:", "").strip()
        table, columns = schema.split("; Columns:")
        table = table.strip()
        columns = [col.strip() for col in columns.split(",")]
        schema_info["table"] = table
        schema_info["columns"] = columns
    except Exception as e:
        print(f"Error parsing schema: {e}")
    return schema_info

schema = "Table: pilot; Columns: Pilot_Id, Name, Age"

# Function to clean and validate the generated SQL query
def clean_and_validate_sql(sql_query, schema_info):
    table_name = schema_info.get("table", "")
    valid_columns = schema_info.get("columns", [])
    
    # Remove metadata after '|'
    if "|" in sql_query:
        sql_query = sql_query.split("|")[0].strip()
    
    # Replace generic table name with actual table name
    if "FROM table" in sql_query and table_name:
        sql_query = sql_query.replace("FROM table", f"FROM {table_name}")
    
    # Ensure string literals are quoted
    sql_query = re.sub(r"= ([a-zA-Z]+)", r"= '\1'", sql_query)
    
    # Remove extraneous conditions
    for condition in re.findall(r"AND (.+?=.*?)", sql_query):
        if not any(col in condition for col in valid_columns):
            sql_query = sql_query.replace(f"AND {condition}", "")
    
    # Validate column names
    for col in re.findall(r"SELECT (.+?) FROM", sql_query):
        if col not in valid_columns:
            print(f"Warning: Column '{col}' is not in the schema. Adjusting query...")
            sql_query = sql_query.replace(col, valid_columns[0])  # Use the first valid column
    
    return sql_query.strip()
 
# Function to translate natural language to SQL
def nl_to_sql(nl_query, schema=schema):
    schema_info = parse_schema(schema)
    input_text = (
        f"translate English to SQL: {nl_query} "
        f"using table '{schema_info['table']}' and columns {', '.join(schema_info['columns'])}."
    )
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids
    output_ids = model.generate(input_ids, max_new_tokens=150, num_beams=5, early_stopping=True)
    sql_query = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
    
    # Clean and validate the generated SQL query
    sql_query = clean_and_validate_sql(sql_query, schema_info)
    
    return sql_query
 
# Main program
nl_query = "Who are the pilots above age of 28?"

 
sql_query = nl_to_sql(nl_query, schema)
print(f"Generated SQL: {sql_query}")