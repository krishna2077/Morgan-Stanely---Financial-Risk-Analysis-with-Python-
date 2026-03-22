
#Task 6: Hypothesis Testing

# TASK 6-1 --------------------------------------------------------------------

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Clean AccountBalance column
def clean_numeric(val):
    if pd.isna(val): return np.nan
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    try: return float(clean_val)
    except ValueError: return np.nan

df['AccountBalance'] = df['AccountBalance'].apply(clean_numeric)

# Drop rows with missing balances
df = df.dropna(subset=['AccountBalance'])

# Aggregate metrics per Account
account_stats = df.groupby('AccountID').agg(
    Transaction_Count=('TransactionID', 'count'),
    Average_Balance=('AccountBalance', 'mean')
).reset_index()

# Define High vs Low volume based on the median
median_vol = account_stats['Transaction_Count'].median()

# Separate the average balances into two groups
high_vol_bals = account_stats[account_stats['Transaction_Count'] > median_vol]['Average_Balance']
low_vol_bals = account_stats[account_stats['Transaction_Count'] <= median_vol]['Average_Balance']

# Perform Independent T-Test (One-tailed test: High > Low)
t_stat, p_value = stats.ttest_ind(high_vol_bals, low_vol_bals, alternative='greater')

print(f"High Vol Mean: ${high_vol_bals.mean():,.2f}")
print(f"Low Vol Mean: ${low_vol_bals.mean():,.2f}")
print(f"T-Statistic: {t_stat:.4f} | P-Value: {p_value:.4f}")

# TASK 6-2 --------------------------------------------------------------------

import pandas as pd
import scipy.stats as stats

# Load and clean the data
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

def clean_numeric(val):
    if pd.isna(val): return np.nan
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    try: return float(clean_val)
    except: return np.nan

df['AccountBalance'] = df['AccountBalance'].apply(clean_numeric)
df['CreditRating'] = pd.to_numeric(df['CreditRating'], errors='coerce')
df['RiskScore'] = pd.to_numeric(df['RiskScore'], errors='coerce')

# Aggregate metrics by Customer
customer_df = df.groupby('CustomerID').agg(
    Avg_Balance=('AccountBalance', 'mean'),
    Avg_CreditRating=('CreditRating', 'mean'),
    Avg_RiskScore=('RiskScore', 'mean')
).dropna().reset_index()

# Segment Customers by Average Balance (33rd & 66th percentiles)
b_low, b_high = customer_df['Avg_Balance'].quantile([0.33, 0.66])

def get_balance_segment(val):
    if val <= b_low: return 'Low'
    elif val <= b_high: return 'Medium'
    else: return 'High'

customer_df['Balance_Segment'] = customer_df['Avg_Balance'].apply(get_balance_segment)


# One-Way ANOVA (Credit Rating across all 3 segments)
low_credit = customer_df[customer_df['Balance_Segment'] == 'Low']['Avg_CreditRating']
med_credit = customer_df[customer_df['Balance_Segment'] == 'Medium']['Avg_CreditRating']
high_credit = customer_df[customer_df['Balance_Segment'] == 'High']['Avg_CreditRating']

f_stat, p_value_anova = stats.f_oneway(low_credit, med_credit, high_credit)

print(f"ANOVA F-Stat: {f_stat:.4f} | P-Value: {p_value_anova:.4f}")
if p_value_anova < 0.05:
    print("Result: Significant difference in Credit Ratings.")
else:
    print("Result: NO significant difference in Credit Ratings.")

# Independent T-Test (Risk Score: High vs Low Balance)
low_risk = customer_df[customer_df['Balance_Segment'] == 'Low']['Avg_RiskScore']
high_risk = customer_df[customer_df['Balance_Segment'] == 'High']['Avg_RiskScore']

t_stat, p_value_ttest = stats.ttest_ind(high_risk, low_risk)

print(f"\nT-Test T-Stat: {t_stat:.4f} | P-Value: {p_value_ttest:.4f}")
if p_value_ttest < 0.05:
    print("Result: High Balance Risk Score is significantly different.")
else:
    print("Result: High Balance Risk Score is NOT significantly different.")




















