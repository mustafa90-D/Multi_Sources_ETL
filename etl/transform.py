import pandas as pd
import requests
def transform_data(sales, customers, products, gov=None):
    sales['sale_date'] = pd.to_datetime(sales['sale_date'])
    sales['month'] = sales['sale_date'].dt.month
    sales['year'] = sales['sale_date'].dt.year

    # Merge with customer and product category (not price)
    df = sales.merge(customers, on="customer_id") \
              .merge(products[['product', 'category']], on="product", how="left")

    # Calculate total sales from sales.csv
    df['total_sales'] = df['quantity'] * df['price']
    return df

# ========== etl/transform.py ==========
def clean_dummyjson_products(df):
    df = df[["id", "title", "price", "stock", "brand", "category", "rating", "discountPercentage"]]
    df.columns = [col.lower() for col in df.columns]
    return df

def clean_redmi_data(df):
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    df = df.dropna()

    # Extract numeric rating (e.g., "4.0 out of 5 stars" → 4.0)
    if "rating" in df.columns:
        df["rating"] = df["rating"].str.extract(r"(\d+(\.\d+)?)").astype(float)

    return df



    # # Optional gov merge
    # if gov is not None:
    #     gov.columns = [col.lower().replace(" ", "_") for col in gov.columns]
    #     gov = gov.rename(columns={"sales": "external_sales"})
    #     gov['year'] = pd.to_datetime(gov['date']).dt.year
    #     gov['month'] = pd.to_datetime(gov['date']).dt.month
    #     df = df.merge(gov[['month', 'year', 'external_sales']], on=["month", "year"], how="left")
    #     df['external_sales'] = df['external_sales'].fillna(0)

    # return df
