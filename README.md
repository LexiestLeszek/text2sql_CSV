# Text2SQL_CSV 

## Introduction

The Text2SQL CSV project is a Python-based application designed to facilitate the conversion of natural language queries into SQL queries and execute these queries on a SQLite database. This project leverages the power of Large Language Models (LLMs) to interpret user input and generate SQL queries, enabling users to interact with their data in a more natural and intuitive manner.

## Installation

Clone the repo:

```bash
git clone https://github.com/LexiestLeszek/text2sql_CSV.git
```

Then install the necessary Python libraries, run the following command:

```bash
pip install pandas sqlite3 llmware
```

## Usage

1. **Upload CSV to SQLite**: Use the `upload_csv_to_sqlite` function to upload a CSV file to a SQLite database. This function reads the CSV file, creates a table in the SQLite database with the same name as the CSV file, and inserts the data from the CSV file into the table.

    ```python
    db_schema = upload_csv_to_sqlite('./StockRatings.csv', './StockRatings.db')
    ```

2. **Text to SQL**: Use the `text2sql` function to convert a natural language query into an SQL query. This function uses the LLM to interpret the query and generate an SQL query.

    ```python
    query_sql = text2sql('Who has the best overall rating?', db_schema)
    ```

3. **Query Database**: Use the `query_db` function to execute the generated SQL query on the SQLite database and retrieve the results.

    ```python
    answer = query_db(query_sql, './StockRatings.db')
    print(answer)
    ```

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
