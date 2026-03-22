
#Task 4: Financial Risk Identification

# TASK 4-1---------------------------------------------------------------------

import pandas as pd
import re

# Load data
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Clean Financial Fields
def clean_numeric(val):
    if pd.isna(val): return 0.0
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    return float(clean_val) if clean_val else 0.0

df['TransactionAmount'] = df['TransactionAmount'].apply(clean_numeric)
df['AccountBalance'] = df['AccountBalance'].apply(clean_numeric)

# Standardize Transaction Type
df['TransactionType'] = df['TransactionType'].str.strip().str.title()

# Identifying Large Withdrawals
withdrawals = df[df['TransactionType'] == 'Withdrawal']
# Defining threshold at 90th percentile
threshold = withdrawals['TransactionAmount'].quantile(0.90)

large_withdrawals = withdrawals[withdrawals['TransactionAmount'] > threshold]
large_counts = large_withdrawals['AccountID'].value_counts().reset_index()
large_counts.columns = ['AccountID', 'Large_Withdrawal_Count']

# Identifying Overdrafts
overdrafts = df[df['AccountBalance'] < 0]
overdraft_counts = overdrafts['AccountID'].value_counts().reset_index()
overdraft_counts.columns = ['AccountID', 'Overdraft_Count']

# Combine & Report
report = pd.merge(large_counts, overdraft_counts, on='AccountID', how='outer').fillna(0)
report['Large_Withdrawal_Count'] = report['Large_Withdrawal_Count'].astype(int)
report['Overdraft_Count'] = report['Overdraft_Count'].astype(int)

# Sort by severity
report = report.sort_values(['Overdraft_Count', 'Large_Withdrawal_Count'], ascending=False)

print(f"Large Withdrawal Threshold (90th percentile): ${threshold:,.2f}")
print(report.head(10).to_markdown(index=False))

# Save results
report.to_csv('suspicious_account_activity.csv', index=False)

# TASK 4-2 --------------------------------------------------------------------

import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Clean AccountBalance column
def clean_currency(val):
    if pd.isna(val): return np.nan
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    try:
        return float(clean_val)
    except ValueError:
        return np.nan

df['AccountBalance'] = df['AccountBalance'].apply(clean_currency)

# Calculate Volatility Metrics
volatility = df.groupby('AccountID')['AccountBalance'].agg(['std', 'mean']).reset_index()

# Calculate Coefficient of Variation (CV)
# CV = Standard Deviation / Mean
volatility['Coefficient_of_Variation'] = volatility['std'] / volatility['mean']

# Rename columns
volatility.columns = ['AccountID', 'Balance_Std_Dev', 'Average_Balance', 'CV']

# Filter out accounts with insufficient data (std is NaN) and sort
volatility = volatility.dropna(subset=['Balance_Std_Dev']).sort_values(by='CV', ascending=False)

# Save results
volatility.to_csv('account_balance_volatility.csv', index=False)

print("Top 10 Most Volatile Accounts:")
print(volatility.head(10).to_markdown(index=False))

# TASK 4-4 --------------------------------------------------------------------

import pandas as pd

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Clean Financial Fields
def clean_numeric(val):
    if pd.isna(val): return 0.0
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    try: return float(clean_val)
    except: return 0.0

df['TransactionAmount'] = df['TransactionAmount'].apply(clean_numeric)
df['AccountBalance'] = df['AccountBalance'].apply(clean_numeric)
df['RiskScore'] = pd.to_numeric(df['RiskScore'], errors='coerce')

# Define Suspicion Criteria
# Criteria A: Value Outliers (Z-Score > 2.5)
mean_amt = df['TransactionAmount'].mean()
std_amt = df['TransactionAmount'].std()
df['Is_Value_Anomaly'] = ((df['TransactionAmount'] - mean_amt) / std_amt).abs() > 2.5

# Criteria B: High Risk Score (> 0.8)
df['Is_High_Risk'] = df['RiskScore'] > 0.8

# Criteria C: Overdrafts (Balance < 0)
df['Is_Overdraft'] = df['AccountBalance'] < 0

# Aggregate Flags by Customer
suspicion_report = df.groupby('CustomerID').agg(
    Total_Transactions=('TransactionID', 'count'),
    Anomaly_Count=('Is_Value_Anomaly', 'sum'),
    High_Risk_Txn_Count=('Is_High_Risk', 'sum'),
    Overdraft_Count=('Is_Overdraft', 'sum')
).reset_index()

# Criteria D: High Transaction Frequency (Top 10%)
freq_threshold = suspicion_report['Total_Transactions'].quantile(0.90)
suspicion_report['High_Frequency_Flag'] = suspicion_report['Total_Transactions'] >= freq_threshold

# Calculate Total Red Flags 
suspicion_report['Total_Red_Flags'] = (
    suspicion_report['Anomaly_Count'] + 
    suspicion_report['High_Risk_Txn_Count'] + 
    suspicion_report['Overdraft_Count'] + 
    suspicion_report['High_Frequency_Flag'].astype(int)
)

# Filter and Sort
suspicious_customers = suspicion_report[suspicion_report['Total_Red_Flags'] > 0].sort_values(by='Total_Red_Flags', ascending=False)

# Save to CSV
suspicious_customers.to_csv('suspicious_customer_behavior.csv', index=False)

# Display Top Results
print("Top Customers with Suspicious Behavior:")
print(suspicious_customers.head(10).to_markdown(index=False))










