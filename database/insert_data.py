# insert_data.py
from create_table import engine, dtype_mapping, table_name
import pandas as pd
from cleaning_checkpoint import clean_data

# Suppose `clean_data` is already prepared
# from clean_data import clean_data  

batch_size = 100000
for start in range(0, len(clean_data), batch_size):
    end = start + batch_size
    batch_df = clean_data.iloc[start:end]
    batch_df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False,
        dtype=dtype_mapping
    )
    print(f"Inserted rows {start} to {min(end, len(clean_data))}")

print("Data successfully inserted into MySQL!")
