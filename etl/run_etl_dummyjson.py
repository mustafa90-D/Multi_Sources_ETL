import requests
import pandas as pd
from extract import fetch_dummyjson_products
from transform import clean_dummyjson_products
from load import load_products_to_db

DUMMYJSON_URL = "https://dummyjson.com/products"
DB_PATH = "../db/retail_sales.db"

def run():
    df_raw = fetch_dummyjson_products(DUMMYJSON_URL)
    df_clean = clean_dummyjson_products(df_raw)
    load_products_to_db(df_clean, DB_PATH)
    print(" ETL_Dummyjason Completed!")

if __name__ == "__main__":
    run()

