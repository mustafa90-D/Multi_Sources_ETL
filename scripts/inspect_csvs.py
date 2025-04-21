import pandas as pd

sales = pd.read_csv("../data/raw/sales.csv")
products = pd.read_csv("../data/raw/products.csv")

print("🧾 Sales columns:", sales.columns.tolist())
print("📦 Products columns:", products.columns.tolist())

print("\n🔍 Sample sales data:")
print(sales.head())

print("\n🔍 Sample product data:")
print(products.head())
