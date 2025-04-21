import sqlite3

def load_to_sqlite(df, sales, customers, products, db_path):
    conn = sqlite3.connect(db_path)
    sales.to_sql("sales", conn, if_exists="replace", index=False)
    customers.to_sql("customers", conn, if_exists="replace", index=False)
    products.to_sql("products", conn, if_exists="replace", index=False)
    df.to_sql("retail_analytics", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

def load_redmi_to_db(df, db_path):
    with sqlite3.connect(db_path) as conn:
        df.to_sql("redmi_specs", conn, if_exists="replace", index=False)

def load_redmi_to_db(df, db_path):
    with sqlite3.connect(db_path) as conn:
        df.to_sql("redmi6_specs", conn, if_exists="replace", index=False)