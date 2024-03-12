from llmware.agents import LLMfx
import pandas as pd
#from llmware.models import ModelCatalog
#ModelCatalog().get_llm_toolkit(["sql"])

def main():
    
    csv_file_path = "StockRatings.csv"
    
    query = "What are the companies with the best overall rating?"
    
    df = pd.read_csv(csv_file_path)
                
    column_names = df.columns.tolist()
    data_type = "" ## TODO: Add datatype identification logic
    column_names_string = ', '.join([f'{name} {data_type}' for name in column_names])
    table_name = csv_file_path.split('/')[-1].split('.')[0]
    schema_from_csv = f"CREATE TABLE {table_name} ({column_names_string})"

    agent = LLMfx(verbose=False)
    response_json = agent.sql(query, schema_from_csv)
    
    response = response_json['llm_response']

    print(response)

    return response

if __name__ == "__main__":
    
    main()
