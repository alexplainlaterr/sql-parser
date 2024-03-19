import pandas as pd
from pathlib import Path
from sql_metadata import Parser

def process_sql_queries(df):
    # Initialize an empty set to store all tables
    all_tables = set()

    for index, row in df.iterrows():
        sql_query = row['sql_unload']
        try:
            tables = Parser(sql_query).tables
            if tables is not None:
                all_tables.update(tables)
                print(f"Query {index + 1}:")
                print(tables)
                print()
            else:
                print(f"Unable to parse query {index + 1}")
                print()
        except Exception as e:
            print(f"Error parsing query {index + 1}: {e}")
            print()

    # Filter out table names that don't contain a period
    all_tables_with_period = {table for table in all_tables if '.' in table}

    # Convert the set of tables to a list and sort it alphabetically
    all_tables_list = sorted(list(all_tables_with_period))

    # Print the distinct list of tables
    print("Distinct list of tables:")
    for table in all_tables_list:
        print(table)

# Real usage:
directory = Path(r'/Users/Alex.Wong/Documents/GitHub/sql-parser')
df = pd.read_excel(directory/'editor-2-queries.xlsx')
process_sql_queries(df)

