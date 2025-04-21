import pandas as pd

# Load CSV
df = pd.read_csv("C:/Users/mustafa.tark/Downloads/archive/retail_sales_dataset.csv")

# Clean column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
print("Cleaned columns:", df.columns.tolist())

# === Save sales ===
sales = df[['transaction_id', 'customer_id', 'product_category', 'quantity', 'price_per_unit', 'date']].copy()
sales.rename(columns={
    'transaction_id': 'invoice_id',
    'product_category': 'product',
    'price_per_unit': 'price',
    'date': 'sale_date'
}, inplace=True)
sales['sale_date'] = pd.to_datetime(sales['sale_date'])
sales.to_csv("../data/raw/sales.csv", index=False)

# === Save customers ===
customers = df[['customer_id', 'age', 'gender']].drop_duplicates()
customers.to_csv("../data/raw/customers.csv", index=False)

# === Save products ===
products = df[['product_category', 'price_per_unit']].drop_duplicates()
products.rename(columns={
    'product_category': 'product',
    'price_per_unit': 'price'
}, inplace=True)
products['category'] = products['product']  # No extra category column
products['product_id'] = range(1, len(products) + 1)
products.to_csv("../data/raw/products.csv", index=False)

print(" Created sales.csv, customers.csv, products.csv")
