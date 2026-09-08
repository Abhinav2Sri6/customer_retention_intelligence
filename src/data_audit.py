from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = PROJECT_ROOT / "data" / "raw"

customer_df = pd.read_csv(RAW_DATA / "telecom_customer_churn.csv")
zipcode_df = pd.read_csv(RAW_DATA / "telecom_zipcode_population.csv")
dictionary_df = pd.read_csv(
    RAW_DATA / "telecom_data_dictionary.csv",
    encoding="cp1252"
)

#------ Viewing the data ------
print("Customer data shape:", customer_df.shape)
print("Zipcode data shape:", zipcode_df.shape)
print("Dictionary shape:", dictionary_df.shape)

print("\nCustomer columns:")
print(customer_df.columns.tolist())

print("\nFirst five rows:")
print(customer_df.head())

print("\nData types:")
print(customer_df.dtypes)

print("\nMissing values:")
print(customer_df.isnull().sum())

print("\nDuplicate rows:")
print(customer_df.duplicated().sum())

print("\nChurn distribution:")
print(customer_df["Customer Status"].value_counts())

#------Create Data Cleaning Plan------

'''Should produce 7043 unique customer IDs'''
print("\nUnique customer IDs:")
print(customer_df["Customer ID"].nunique())

'''Seeking to explain the missing values associated with internet service.
All rows with 1526 missing values correspond to internet service. If we 
observe 1526 people without internet, those missing values do not need
to be discarded.'''
print("\nInternet Service distribution:")
print(customer_df["Internet Service"].value_counts())

'''Same logic as the internet service'''
print("\nPhone Service distribution:")
print(customer_df["Phone Service"].value_counts())

'''NaN in this case most likely means that these customers did not receive
an offer, meaning they could not churn. We use dropna to indicate how
many did not receive the offer.'''
print("\nOffer values:")
print(customer_df["Offer"].value_counts(dropna=False))


print("\nContract values:")
print(customer_df["Contract"].value_counts())

print("\nPayment Method values:")
print(customer_df["Payment Method"].value_counts())

'''Creating a series of true false indices, where only the rows of people
without internet service are considered'''
print("\nInternet fields for customers without internet:")
no_internet = customer_df[customer_df["Internet Service"] == "No"]
print("Customers without internet:", len(no_internet))
print(no_internet[
    [
        "Internet Type",
        "Online Security",
        "Online Backup",
        "Streaming TV"
    ]
].isnull().sum())

'''Fields for customers without internet must be null for these
specific fields, so we should see these values align with the missing
values from earlier.'''
print("\nPhone fields for customers without phone service:")
no_phone = customer_df[customer_df["Phone Service"] == "No"]

print("Customers without phone service:", len(no_phone))

print(no_phone[
    [
        "Avg Monthly Long Distance Charges",
        "Multiple Lines"
    ]
].isnull().sum())

'''Here we look for things like Impossible ages, negative charges,
strange tenure values, extreme revenue, and any other outliers.'''
print("\nNumerical summary:")
print(customer_df[
    [
        "Age",
        "Number of Dependents",
        "Number of Referrals",
        "Tenure in Months",
        "Monthly Charge",
        "Total Charges",
        "Total Revenue"
    ]
].describe())