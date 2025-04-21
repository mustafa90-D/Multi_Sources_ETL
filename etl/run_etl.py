from pathlib import Path
from extract import load_kaggle_data
from transform import transform_data
from load import load_to_sqlite

raw_path = Path("../data/raw")
db_path = Path("../db/retail_sales.db")

sales, customers, products = load_kaggle_data(raw_path)
df = transform_data(sales, customers, products)
load_to_sqlite(df, sales, customers, products, db_path)

print(" ETL Pipeline Completed!")