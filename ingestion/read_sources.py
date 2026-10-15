"""Read the CSV and JSON sources and print their structure."""
import pandas as pd

customers = pd.read_csv("data/source/customers.csv")
products = pd.read_json("data/source/products.json")
sales = pd.read_csv("data/source/sales.csv")

for name, df in [("customers", customers), ("products", products), ("sales", sales)]:
    print(f"\n===== {name.upper()} =====")
    print("Rows, columns:", df.shape)
    print(df.dtypes)
    print(df.head(3))
    print("Nulls per column:")
    print(df.isna().sum())
