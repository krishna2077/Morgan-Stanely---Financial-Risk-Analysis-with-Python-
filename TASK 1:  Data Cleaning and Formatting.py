
#Task 1: Data Cleaning and Formatting 

# TASK 1-1 --------------------------------------------------------------------

import pandas as pd

# Loading the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv', dtype=str)

# Define the financial columns to clean
financial_cols = ['TransactionAmount', 'AccountBalance']

def clean_financial_field(value):
    #Returns NaN if the value is missing or cannot be converted.
    if pd.isna(value):
        return value
    # Remove characters that are NOT 0-9, '.', or '-'
    clean_val = re.sub(r'[^0-9.-]','', str(value))
    return clean_val

# Apply the cleaning function and convert to numeric
for col in financial_cols:
    # Clean the string
    df[col] = df[col].apply(clean_financial_field)
    # Convert to numeric
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Save the cleaned data to a new CSV file
df.to_csv('morgan_stanely_cleaned.csv', index=False)

# Verify the results
print(df[financial_cols].head())
print(df[financial_cols].info())

# TASK 1-2 --------------------------------------------------------------------

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Define currency columns
currency_cols = ['TransactionAmount', 'AccountBalance']

# Convert to numerical format by removing non-numeric characters
for col in currency_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^\d.-]', '', regex=True), errors='coerce')

# Preview the cleaned numerical data
print(df[currency_cols].head())

# TASK 1-3 --------------------------------------------------------------------

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Convert TransactionDate to datetime objects (handling DD-MM-YYYY format)
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], dayfirst=True, errors='coerce')

# Format the dates to YYYY-MM-DD string format
df['TransactionDate'] = df['TransactionDate'].dt.strftime('%Y-%m-%d')

# Save the updated dataframe
df.to_csv('morgan_stanely_formatted_dates.csv', index=False)
print(df['TransactionID'],df['TransactionDate'])

# TASK 1-4 --------------------------------------------------------------------import pandas as pd

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# List of categorical columns to standardize
cols_to_standardize = ['AccountType', 'TransactionType', 'Product']

for col in cols_to_standardize:
    # Remove whitespace and apply Title Case for uniformity
    df[col] = df[col].astype(str).str.strip().str.title()

# Save the updated file
df.to_csv('morgan_stanely_standardized.csv', index=False)
print(df['AccountType'],df['TransactionType'])




