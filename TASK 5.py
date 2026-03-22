
#Task 5: Visualisation

# TASK 5-1 --------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Set plotting style
sns.set_theme(style="whitegrid", palette="muted")

# Load and clean data
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], dayfirst=True, errors='coerce')

def clean_numeric(val):
    if pd.isna(val): return np.nan
    clean_val = re.sub(r'[^0-9.-]', '', str(val))
    try: return float(clean_val)
    except: return np.nan

df['TransactionAmount'] = df['TransactionAmount'].apply(clean_numeric)
df['AccountBalance'] = df['AccountBalance'].apply(clean_numeric)
df['RiskScore'] = pd.to_numeric(df['RiskScore'], errors='coerce')
df['CreditRating'] = pd.to_numeric(df['CreditRating'], errors='coerce')

categorical_cols = ['AccountType', 'TransactionType', 'Product', 'Region']
for col in categorical_cols:
    df[col] = df[col].astype(str).str.strip().str.title()

# Distributions
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df['TransactionAmount'], bins=30, kde=True, ax=axes[0], color='skyblue')
axes[0].set_title('Distribution of Transaction Amount')
sns.histplot(df['AccountBalance'], bins=30, kde=True, ax=axes[1], color='lightcoral')
axes[1].set_title('Distribution of Account Balance')
plt.savefig('eda_distributions.png')

# Categorical Counts
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.countplot(x='TransactionType', data=df, ax=axes[0], palette='viridis')
sns.countplot(x='Region', data=df, ax=axes[1], palette='magma')
sns.countplot(x='Product', data=df, ax=axes[2], palette='cubehelix')
plt.savefig('eda_categorical.png')

# Relationships
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.scatterplot(x='CreditRating', y='RiskScore', hue='AccountType', data=df, ax=axes[0])
sns.boxplot(x='Product', y='TransactionAmount', data=df, ax=axes[1])
plt.savefig('eda_relationships.png')

# Correlation Matrix
plt.figure(figsize=(8, 6))
corr = df[['TransactionAmount', 'AccountBalance', 'RiskScore', 'CreditRating', 'TenureMonths']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.savefig('eda_correlation.png')
