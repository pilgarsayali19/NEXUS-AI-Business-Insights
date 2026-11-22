import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("data/sales.db")

# Load cleaned sales data
df = pd.read_csv("data/sales_data_cleaned.csv")

# Store data in SQL table
df.to_sql("sales", conn, if_exists="replace", index=False)

print("Data successfully stored in SQLite database!")

# Verify records
result = pd.read_sql("SELECT * FROM sales LIMIT 5", conn)

print(result)

conn.close()