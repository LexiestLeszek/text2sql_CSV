from llmware.agents import LLMfx
import pandas as pd
import sqlite3
from sqlite3 import Error

###########################################################
# RUN THIS THING ONCE TO DOWNLOAD LOACL LLMs FROM LLM_WARE:

from llmware.models import ModelCatalog

ModelCatalog().get_llm_toolkit(["sql"])

ModelCatalog().tool_test_run("slim-sql-tool")

###########################################################
###########################################################

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
        schema_string += f'"{column[1]}",'
    
    db_schema = f"CREATE TABLE {table_name} ({schema_string})"
    
    #print("DB SCHEMA:\n\n")
    #print(db_schema)
    
    conn.close()
    
    return db_schema

def text2sql(query, db_schema):
    
    print(db_schema)
    
    agent = LLMfx(verbose=False)
    response_json = agent.sql(query, db_schema)
    
    response = response_json["llm_response"]
    
    print(response)

    return response

def query_db(query, db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
    except Error as e:
        print(e)
        rows = None
    finally:
        if conn:
            conn.close()
    return rows

if __name__ == "__main__":

    csv_file_path = './StockRatings.csv' 
    db_file_path = csv_file_path.replace(".csv", ".db")
    db_schema = upload_csv_to_sqlite(csv_file_path, db_file_path)

    while True:
        
        query_txt = input("Your query: ")
    
        query_sql = text2sql(query_txt, db_schema)
        
        answer = query_db(query_sql,db_file_path)
        
        print("Answer:")
        print(answer)
