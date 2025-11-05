import pandas as pd
import mysql.connector
from datetime import datetime

# Load raw data
raw_data_path = "../data/raw.json"
data = pd.read_json(raw_data_path)

# Data Cleaning / Transformation
data['price'] = pd.to_numeric(data.get('price', 0), errors='coerce').fillna(0)
data['bedrooms'] = pd.to_numeric(data.get('bedrooms', 0), errors='coerce').fillna(0)
data['bathrooms'] = pd.to_numeric(data.get('bathrooms', 0), errors='coerce').fillna(0)
data['area_sqft'] = pd.to_numeric(data.get('area_sqft', 0), errors='coerce').fillna(0)
data['hoa_fee'] = pd.to_numeric(data.get('hoa_fee', 0), errors='coerce').fillna(0)
data['estimated_cost'] = pd.to_numeric(data.get('estimated_cost', 0), errors='coerce').fillna(0)
data['valuation_amount'] = pd.to_numeric(data.get('valuation_amount', 0), errors='coerce').fillna(0)
data['valuation_date'] = pd.to_datetime(data.get('valuation_date', datetime.today()), errors='coerce')

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',  # Update if different
    database='property_db'
)
cursor = conn.cursor()

# Insert into properties
for _, row in data.iterrows():
    cursor.execute("""
        INSERT INTO properties (property_id, address, city, state, zip_code, property_type, bedrooms, bathrooms, area_sqft, price)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE price=%s
    """, (
        row['id'], row['address'], row['city'], row['state'], row['zip_code'],
        row['property_type'], row['bedrooms'], row['bathrooms'], row['area_sqft'], row['price'],
        row['price']
    ))

# Insert into HOA table
for _, row in data.iterrows():
    if row['hoa_fee'] > 0:
        cursor.execute("""
            INSERT INTO hoa (property_id, hoa_fee)
            VALUES (%s,%s)
        """, (row['id'], row['hoa_fee']))

# Insert into Rehab Estimates table
for _, row in data.iterrows():
    if row['estimated_cost'] > 0:
        cursor.execute("""
            INSERT INTO rehab_estimates (property_id, estimated_cost, last_updated)
            VALUES (%s,%s,%s)
        """, (row['id'], row['estimated_cost'], datetime.today().date()))

# Insert into Valuations table
for _, row in data.iterrows():
    if row['valuation_amount'] > 0:
        cursor.execute("""
            INSERT INTO valuations (property_id, valuation_amount, valuation_date)
            VALUES (%s,%s,%s)
        """, (row['id'], row['valuation_amount'], row['valuation_date'].date()))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("ETL Completed Successfully!")
