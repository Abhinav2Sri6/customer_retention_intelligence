from pathlib import Path
import pandas as pd
import sqlite3

from pandas.core.methods.selectn import SelectN

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
RAW_DATA = PROJECT_ROOT / "data" / "raw"
DATABASE_DIR = PROJECT_ROOT / "database"

DATABASE_DIR.mkdir(exist_ok = True)

customer_df = pd.read_csv(PROCESSED_DATA / "telecom_customer_clean.csv")
zipcode_df = pd.read_csv(RAW_DATA / "telecom_zipcode_population.csv")

database_path = DATABASE_DIR / "customer_retention.db"
connection = sqlite3.connect(database_path)

'''Using pandas to populate the database right now. Will use SQL to query it
later.'''
customers = customer_df[
    [
        "Customer ID", "Gender",
        "Age", "Married",
        "Number of Dependents",
        "Number of Referrals",
        "Tenure in Months",
        "Customer Status",
        "Churn", "Churn Category",
        "Churn Reason", "Zip Code"
    ]
].copy()

'''rename to snake_case'''
customers.columns = [
    "customer_id", "gender",
    "age", "married",
    "number_of_dependents",
    "number_of_referrals",
    "tenure_months",
    "customer_status",
    "churn", "churn_category",
    "churn_reason", "zip_code"
]


'''writing in SQL'''
customers.to_sql(
    "customers",
    connection,
    if_exists = "replace",
    index = False
)

'''checking if it worked properly'''
print("\nCustomers table preview:")

result = pd.read_sql_query(
    "SELECT * FROM customers LIMIT 5;",
    connection
)

print(result)

'''Proceeding with other columns'''
services = customer_df[
    [
        "Customer ID",
        "Phone Service",
        "Avg Monthly Long Distance Charges",
        "Multiple Lines",
        "Internet Service",
        "Internet Type",
        "Avg Monthly GB Download",
        "Online Security",
        "Online Backup",
        "Device Protection Plan",
        "Premium Tech Support",
        "Streaming TV",
        "Streaming Movies",
        "Streaming Music",
        "Unlimited Data"
    ]
].copy()

services.columns = [
    "customer_id",
    "phone_service",
    "avg_monthly_long_distance_charges",
    "multiple_lines",
    "internet_service",
    "internet_type",
    "avg_monthly_gb_download",
    "online_security",
    "online_backup",
    "device_protection_plan",
    "premium_tech_support",
    "streaming_tv",
    "streaming_movies",
    "streaming_music",
    "unlimited_data"
]

services.to_sql(
    "customer_services",
    connection,
    if_exists="replace",
    index=False
)

print("Customer and Service Information: ")
query = """
SELECT 
    c.customer_id,
    c.age,
    c.customer_status,
    s.internet_service,
    s.internet_type
FROM customers AS c
JOIN customer_services AS s 
     ON c.customer_id = s.customer_id
LIMIT 10;
"""

results = pd.read_sql_query(query, connection)
print(results)

'''creating the accounts table'''
accounts = customer_df[
    [
        "Customer ID",
        "Offer",
        "Contract",
        "Paperless Billing",
        "Payment Method",
        "Monthly Charge",
        "Monthly Charge Invalid",
        "Total Charges",
        "Total Refunds",
        "Total Extra Data Charges",
        "Total Long Distance Charges",
        "Total Revenue"
    ]
].copy()

accounts.columns = [
    "customer_id",
    "offer",
    "contract",
    "paperless_billing",
    "payment_method",
    "monthly_charge",
    "monthly_charge_invalid",
    "total_charges",
    "total_refunds",
    "total_extra_data_charges",
    "total_long_distance_charges",
    "total_revenue"
]

accounts.to_sql(
    "customer_accounts",
    connection,
    if_exists="replace",
    index=False
)

query = """
SELECT 
    a.contract,
    COUNT(*) AS number_of_customers,
    ROUND(AVG(a.monthly_charge), 2) AS monthly_charge
FROM customer_accounts AS a
GROUP BY a.contract
ORDER BY number_of_customers DESC;
"""

results = pd.read_sql_query(query, connection)
print("\nCustomers by Contract: ")
print(results)

'''Create location table'''
locations = customer_df[
    [
        "Zip Code",
        "City",
        "Latitude",
        "Longitude"
    ]
].drop_duplicates().copy()


locations = locations.rename(columns={
    "Zip Code": "zip_code",
    "City": "city",
    "Latitude": "latitude",
    "Longitude": "longitude"
})

# Rename population dataset columns
zipcode_df = zipcode_df.rename(columns={
    "Zip Code": "zip_code",
    "Population": "population"
})


locations = locations.merge(
    zipcode_df,
    on="zip_code",
    how="left"
)

print("\nLocations preview:")
print(locations.head())

locations.to_sql(
    "locations",
    connection,
    if_exists="replace",
    index=False
)

connection.close()