import pandas as pd
from pathlib import Path
import requests
import boto3
import pandas as pd
from io import StringIO

def load_kaggle_data(raw_path):
    sales = pd.read_csv(raw_path / "sales.csv")
    customers = pd.read_csv(raw_path / "customers.csv")
    products = pd.read_csv(raw_path / "products.csv")
    return sales, customers, products

def fetch_dummyjson_products(url: str) -> pd.DataFrame:
    response = requests.get(url)
    products = response.json().get("products", [])
    return pd.json_normalize(products)

def fetch_csv_from_s3(bucket_name, file_key):
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(StringIO(obj["Body"].read().decode("ISO-8859-1")))

    return df