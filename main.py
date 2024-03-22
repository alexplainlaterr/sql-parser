import pandas as pd
from pathlib import Path
from sql_metadata import Parser

def process_sql_queries(df):
    # Initialize an empty list to store all tables
    all_tables = []

    for index, row in df.iterrows():
        sql_query = row['sql_unload']
        try:
            tables = Parser(sql_query).tables
            if tables is not None:
                # Extend the list with tables from the current query that contain a period in the name
                all_tables.extend(table for table in tables if '.' in table)
                print(f"Query {index + 1}:")
                print(tables)
                print()
            else:
                print(f"Unable to parse query {index + 1}")
                print()
        except Exception as e:
            print(f"Error parsing query {index + 1}: {e}")
            print()

    # Convert the set of tables to a list and sort it alphabetically
    all_tables_list = sorted(list(all_tables))

    # Convert list to data frame
    df = pd.DataFrame({'col': all_tables_list})

    # Count table occurrence
    grouped_df = df.groupby('col').size().reset_index(name='count')
    sorted_df = grouped_df.sort_values(by='count', ascending=False)
    print(sorted_df)


# Real usage:
directory = Path(r'/Users/Alex.Wong/Documents/GitHub/sql-parser')
df = pd.read_excel(directory/'editor-2-queries.xlsx')
process_sql_queries(df)

