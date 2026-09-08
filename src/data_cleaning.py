from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DATA = PROJECT_ROOT / 'data' / 'processed'

customer_df = pd.read_csv(RAW_DATA / 'telecom_customer_churn.csv')
clean_df = customer_df.copy()

'''Assuming NaN in the "Offer" column indicated no offer was given.'''
clean_df["Offer"] = clean_df["Offer"].fillna("No offer")

internet_categorical = ["Internet Type", "Online Security",
                        "Online Backup", "Device Protection Plan",
                        "Premium Tech Support", "Streaming TV",
                        "Streaming Music", "Streaming Movies",
                        "Unlimited Data"]

'''As seen in data_audit, all internet categories align in terms of missing values, 
so I can group them together and assume NaN implies that a customer does not have
internet. This grouping makes it easier for the SQL and ML preprocessing later on'''
clean_df[internet_categorical] = clean_df[internet_categorical].fillna("Not Applicable")

'''Same logic applies here for phone billing'''
clean_df["Avg Monthly GB Download"] = clean_df["Avg Monthly GB Download"].fillna(0)
clean_df["Multiple Lines"] = clean_df["Multiple Lines"].fillna("Not Applicable")
clean_df["Avg Monthly Long Distance Charges"] = clean_df["Avg Monthly Long Distance Charges"].fillna(0)

'''Creating the ML target with a new binary column called "Churn". Not including "Joined"
on purpose, as the modeling data set can just exclude customers where churn is missing.'''
clean_df["Churn"] = clean_df["Customer Status"].map ({
    "Stayed": 0,
    "Churned": 1
})

'''Checking results'''
print("Missing values after cleaning:")
print(clean_df.isnull().sum())

print("\nChurn Target: ")
print(clean_df["Churn"].value_counts(dropna = False))


numeric_check_columns = [
    "Age",
    "Number of Dependents",
    "Number of Referrals",
    "Tenure in Months",
    "Avg Monthly Long Distance Charges",
    "Avg Monthly GB Download",
    "Monthly Charge",
    "Total Charges",
    "Total Refunds",
    "Total Extra Data Charges",
    "Total Long Distance Charges",
    "Total Revenue"
]

'''Sanity Checking  results for erroneous values such as negative or
extreme values'''
print("\nNumerical summary:")
print(clean_df[numeric_check_columns].describe().T)

print("Negative value counts: ")
for column in numeric_check_columns:
    negative_count = (clean_df[column] < 0).sum()
    print(f"column: {column}, count: {negative_count}")


print("\nMinimum values:")
print(clean_df[numeric_check_columns].min())
print("\nMaximum values:")
print(clean_df[numeric_check_columns].max())

'''After running the negative value check and a min,max values check, I can see that
there is not any extraordinarily high values, but there are negative charges, 
specifically in the monthly chargest column. I use the loc function to locate
these negative charges.'''
print("\nCustomers with non-positive monthly charges:")
print(
    clean_df.loc[
        clean_df["Monthly Charge"] <= 0,
        [
            "Customer ID",
            "Customer Status",
            "Tenure in Months",
            "Phone Service",
            "Internet Service",
            "Monthly Charge",
            "Total Charges",
            "Total Revenue"
        ]
    ]
)

'''I can build a truth table column to flag these invalid charges, without having to remove
them, showing that they were originally anomalous, and later let the ML preprocessing 
pipeline impute them properly.'''
clean_df["Monthly Charge Invalid"] = (
    clean_df["Monthly Charge"] < 0
).astype(int)

# Replace invalid monthly charges with missing values
clean_df.loc[
    clean_df["Monthly Charge"] < 0,
    "Monthly Charge"
] = pd.NA

clean_df.to_csv(PROCESSED_DATA / 'telecom_customer_clean.csv', index = False)

'''Validation'''
print("\nInvalid monthly charges flagged:")
print(clean_df["Monthly Charge Invalid"].value_counts())

print("\nMissing monthly charges after cleaning:")
print(clean_df["Monthly Charge"].isnull().sum())