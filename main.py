import pandas as pd
import sqlite3
from sqlite3 import Error
from llmware.agents import LLMfx

###########################################################
# RUN THIS THING ONCE TO DOWNLOAD LOCAL LLMs FROM LLM_WARE:

from llmware.models import ModelCatalog

ModelCatalog().get_llm_toolkit(["sql"])

ModelCatalog().tool_test_run("slim-sql-tool")

###########################################################
###########################################################

def main(csv_file_path):
    
    df = pd.read_csv(csv_file_path)
    
    conn = sqlite3.connect(":MEMORY:")
    
    table_name = csv_file_path.split('/')[-1].split('.')[0]
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    schema = cursor.fetchall()
    
    schema_string = ",".join(f'"{column[1]}"' for column in schema)
    
    db_schema = f"CREATE TABLE {table_name} ({schema_string})"
    
    print(db_schema)
    
    query = "Who has the best overall rating?"

    agent = LLMfx(verbose=False)
    response_json = agent.sql(query, db_schema)
    
    response = response_json["llm_response"]
    
    print(response)
    
    words1 = response.split()
    words2 = db_schema.split()
    
    for i in range(len(words1)):

        if words1[i] in words2 and not (words1[i].startswith('"') and words1[i].endswith('"')):
    
            words1[i] = f'"{words1[i]}"'
    
    modified_string = ' '.join(words1)
    
    try:
        cursor.execute(modified_string)
        rows = cursor.fetchall()
        print(rows)
        return rows
    except Error as e:
        print(e)
        rows = None
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    
    file_path = "./StockRatings.csv"
    
    main(file_path)
    
