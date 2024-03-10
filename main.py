from llmware.agents import LLMfx
import pandas as pd
import sqlite3

def upload_csv_to_sqlite(csv_file_path, db_file_path):
    
    df = pd.read_csv(csv_file_path)
    
    conn = sqlite3.connect(db_file_path)
    
    table_name = csv_file_path.split('/')[-1].split('.')[0]
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    schema = cursor.fetchall()
    
    schema_string = ""
    for column in schema:
        schema_string += f"{column[1]}, "
    
    db_schema = f"CREATE TABLE {table_name} ({schema_string})"
    
    conn.close()
    
    return db_schema

def text2sql(query, db_schema):

    #sample_table_schema = "CREATE TABLE customer_info (customer_name text, account_number integer, annual_spend integer)"

    #query = "What are the names of all customers with annual spend greater than $1000?"
    
    full_schema = db_schema
    
    print(db_schema)
    
    conn = sqlite3.connect(db_file_path)
    
    cursor = conn.cursor()
    
    agent = LLMfx(verbose=False)
    response_json = agent.sql(query, full_schema)
    
    response = response_json["llm_response"]
    
    print(response)

    cursor.execute(response)
    
    rows = cursor.fetchall()
    answer_final = ""
    
    print("Actual Answer:")
    for row in rows:
        print(row)
        answer_final += f'{row}\n'
    
    conn.close()

    return answer_final


if __name__ == "__main__":

    csv_file_path = './StockRatings.csv' 
    db_file_path = './StockRatings.db'
    schema_string = upload_csv_to_sqlite(csv_file_path, db_file_path)

    while True:
        
        query = input("Your query: ")
    
        text2sql(query, schema_string)