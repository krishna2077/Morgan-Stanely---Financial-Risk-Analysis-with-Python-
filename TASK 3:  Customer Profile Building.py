
#Task 3: Customer Profile Building 

# TASK 3-1 --------------------------------------------------------------------

import pandas as pd

# Load the dataset
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Count transactions per account
transaction_counts = df['AccountID'].value_counts().reset_index()
transaction_counts.columns = ['AccountID', 'Transaction_Frequency']

# Define thresholds based on quantiles (33rd and 66th percentiles)
low_threshold = 3
high_threshold = 5

def categorize_activity(freq):
    if freq <= low_threshold:
        return 'Low'
    elif freq <= high_threshold:
        return 'Medium'
    else:
        return 'High'

# Apply categorization
transaction_counts['Activity_Level'] = transaction_counts['Transaction_Frequency'].apply(categorize_activity)

# Rename column to include rubric for clarity
transaction_counts.rename(columns={'Activity_Level': 'Activity_Level (Low <= 3, Medium 4-5, High > 5)'}, inplace=True)

# Display the grouped accounts
print(transaction_counts.head().to_markdown(index=False))

# Save the results
transaction_counts.to_csv('account_activity_levels.csv', index=False)

# TASK 3-2 --------------------------------------------------------------------
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv(r'D:\Course Data DS\COURSE 5 RESOURCES\morgan_stanely.csv')

# Aggregate data by CustomerID
customer_df = df.groupby('CustomerID').agg({
    'AccountBalance': 'mean',
    'TransactionAmount': 'sum'
}).reset_index()

customer_df.columns = ['CustomerID', 'AvgBalance', 'TotalTransactionVolume']

# Scale features
scaler = StandardScaler()
features = ['AvgBalance', 'TotalTransactionVolume']
scaled_features = scaler.fit_transform(customer_df[features])

# Apply K-Means Clustering (k=4)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
customer_df['Cluster'] = kmeans.fit_predict(scaled_features)

# Visualize Clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=customer_df, x='AvgBalance', y='TotalTransactionVolume', hue='Cluster', palette='viridis')
plt.title('Customer Segments: Avg Balance vs Transaction Volume')
plt.xlabel('Average Account Balance')
plt.ylabel('Total Transaction Volume')
plt.savefig('cluster_plot.png')

# Save results
customer_df.to_csv('customer_segments.csv', index=False)

# Display cluster summary
print(customer_df.groupby('Cluster')[features].mean())


















