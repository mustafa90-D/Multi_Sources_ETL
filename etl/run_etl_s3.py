from extract import fetch_csv_from_s3
from transform import clean_redmi_data
from load import load_redmi_to_db

BUCKET = "dashboared"
KEY = "redmi6.csv"
DB_PATH = "../db/retail_sales.db"

def run():
    df_raw = fetch_csv_from_s3(BUCKET, KEY)
    df_clean = clean_redmi_data(df_raw)
    load_redmi_to_db(df_clean, DB_PATH)
    print(" ETL for S3 > SQLite complete.")

if __name__ == "__main__":
    run()
