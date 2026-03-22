
#Task 2: Descriptive Transactional Analysis

# TASK 2-1 --------------------------------------------------------------------

import pandas as pd
import re
# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

#Clean Dates (Handling DD-MM-YYYY format)
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], dayfirst=True, errors='coerce')

# Clean Financial Fields
def clean_numeric(val):
    if pd.isna(val): return 0.0
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    return float(clean_val) if clean_val else 0.0

df['TransactionAmount'] = df['TransactionAmount'].apply(clean_numeric)

# Credits = Deposits | Debits = Withdrawals, Payments, Transfers
df['Type'] = df['TransactionType'].str.strip().str.title()
df['Credit'] = df.apply(lambda x: x['TransactionAmount'] if x['Type'] == 'Deposit' else 0, axis=1)
df['Debit'] = df.apply(lambda x: x['TransactionAmount'] if x['Type'] in ['Withdrawal', 'Payment', 'Transfer'] else 0, axis=1)

# Extract Timeframes
df['Year'] = df['TransactionDate'].dt.year
df['YearMonth'] = df['TransactionDate'].dt.to_period('M')

# Calculate Yearly Summary
yearly_summary = df.groupby('Year').agg(
    Total_Credits=('Credit', 'sum'),
    Total_Debits=('Debit', 'sum')
).reset_index()
yearly_summary['Net_Volume'] = yearly_summary['Total_Credits'] - yearly_summary['Total_Debits']

# Calculate Monthly Summary
monthly_summary = df.groupby('YearMonth').agg(
    Total_Credits=('Credit', 'sum'),
    Total_Debits=('Debit', 'sum')
).reset_index()
monthly_summary['Net_Volume'] = monthly_summary['Total_Credits'] - monthly_summary['Total_Debits']

# Display and Save results
print(yearly_summary)
yearly_summary.to_csv('yearly_summary.csv', index=False)
monthly_summary.to_csv('monthly_summary.csv', index=False)


# TASK 2-2 --------------------------------------------------------------------

import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Clean Dates (Handling DD-MM-YYYY format)
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], dayfirst=True, errors='coerce')

# Clean Financial Fields
def clean_numeric(val):
    if pd.isna(val): return 0.0
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    return float(clean_val) if clean_val else 0.0
df['TransactionAmount'] = df['TransactionAmount'].apply(clean_numeric)

# Categorize Transactions
df['Type'] = df['TransactionType'].str.strip().str.title()
df['Credit'] = df.apply(lambda x: x['TransactionAmount'] if x['Type'] == 'Deposit' else 0, axis=1)
df['Debit'] = df.apply(lambda x: x['TransactionAmount'] if x['Type'] in ['Withdrawal', 'Payment', 'Transfer'] else 0, axis=1)

# Aggregate by Month
df['YearMonth'] = df['TransactionDate'].dt.to_period('M')
trend = df.groupby('YearMonth').agg(
    Total_Credits=('Credit', 'sum'),
    Total_Debits=('Debit', 'sum')
).reset_index().sort_values('YearMonth')

# Convert period to string for plotting
trend['YearMonth'] = trend['YearMonth'].astype(str)

# 6. Plotting
plt.plot(trend['YearMonth'], trend['Total_Credits'], marker='o', label='Total Credits', color='green')
plt.plot(trend['YearMonth'], trend['Total_Debits'], marker='s', label='Total Debits', color='red')

plt.title('Monthly Trends: Total Credits vs. Debits')
plt.xlabel('Month')
plt.ylabel('Amount ($)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Save and display the trend
plt.savefig('financial_trends.png')

# TASK 2-3 --------------------------------------------------------------------

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Clean Financial Fields
def clean_numeric(val):
    if pd.isna(val): return 0.0
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    return float(clean_val) if clean_val else 0.0

df['TransactionAmount'] = df['TransactionAmount'].apply(clean_numeric)

# Credits = Deposits | Debits = Withdrawals, Payments, Transfers
df['Type'] = df['TransactionType'].str.strip().str.title()
df['Credit'] = df.apply(lambda x: x['TransactionAmount'] if x['Type'] == 'Deposit' else 0, axis=1)
df['Debit'] = df.apply(lambda x: x['TransactionAmount'] if x['Type'] in ['Withdrawal', 'Payment', 'Transfer'] else 0, axis=1)

# Group by AccountID and Calculate Net Inflow
performance = df.groupby('AccountID').agg(
    Total_Credits=('Credit', 'sum'),
    Total_Debits=('Debit', 'sum')
).reset_index()

performance['Net_Inflow'] = performance['Total_Credits'] - performance['Total_Debits']

# Identify Top and Bottom Performers
top_10 = performance.sort_values(by='Net_Inflow', ascending=False).head(10)
bottom_10 = performance.sort_values(by='Net_Inflow', ascending=True).head(10)

# Save results
performance.to_csv('account_net_inflow_performance.csv', index=False)

# TASK 2-4 --------------------------------------------------------------------

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Converting TransactionDate to datetime
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], dayfirst=True, errors='coerce')

# Sort by AccountID and Date to calculate gaps correctly
df = df.sort_values(by=['AccountID', 'TransactionDate'])

# Calculate the difference in days
df['Days_Since_Prev_Txn'] = df.groupby('AccountID')['TransactionDate'].diff().dt.days

# Define inactivity threshold (60 days ≈ 2 months)
threshold_days = 60

# --- Flagging Logic ---
historical_gaps = df.groupby('AccountID')['Days_Since_Prev_Txn'].max()

last_txn_date = df.groupby('AccountID')['TransactionDate'].max()
dataset_end_date = df['TransactionDate'].max()
days_since_last = (dataset_end_date - last_txn_date).dt.days

# Combine into a report DataFrame
account_status = pd.DataFrame({
    'Max_Gap_Days': historical_gaps,
    'Last_Txn_Date': last_txn_date,
    'Days_Since_Last_Txn': days_since_last
})

# Create Flags
account_status['Has_History_of_Inactivity'] = account_status['Max_Gap_Days'] >= threshold_days
account_status['Currently_Dormant'] = account_status['Days_Since_Last_Txn'] >= threshold_days
account_status['Is_Flagged'] = account_status['Has_History_of_Inactivity'] | account_status['Currently_Dormant']

# Filter and display flagged accounts
flagged_accounts = account_status[account_status['Is_Flagged']].sort_values(by='Max_Gap_Days', ascending=False)

print(f"Total Accounts Flagged: {len(flagged_accounts)}")
print(flagged_accounts.head(10))

# Save the report
account_status.to_csv('dormant_inactive_accounts.csv')























