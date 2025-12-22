import pandas as pd

# Read the daily sales data CSV file
df0 = pd.read_csv('data/daily_sales_data_0.csv')
df1 = pd.read_csv('data/daily_sales_data_1.csv')
df2 = pd.read_csv('data/daily_sales_data_2.csv')

# Keep only the information we need (Only pink morsel sales, quantity times price)
df0 = df0[df0['product'] == 'pink morsel']
df1 = df1[df1['product'] == 'pink morsel']
df2 = df2[df2['product'] == 'pink morsel']

# Calculate the total sales (price * quantity for each row)
# Remove $ sign and convert price to numeric, then multiply by quantity
df0['sales'] = df0['quantity'] * df0['price'].str.replace('$', '').astype(float)
df1['sales'] = df1['quantity'] * df1['price'].str.replace('$', '').astype(float)
df2['sales'] = df2['quantity'] * df2['price'].str.replace('$', '').astype(float)

# Keep only the columns we need
df0 = df0[['sales', 'date', 'region']]
df1 = df1[['sales', 'date', 'region']]
df2 = df2[['sales', 'date', 'region']]

# Concatenate the three dataframes
df = pd.concat([df0, df1, df2])

# Format total_sales with dollar sign and 2 decimal places
df['sales'] = df['sales'].apply(lambda x: f'${x:.2f}')

# Save the total sales to a CSV file
df.to_csv('data/pink_morsel_sales.csv', index=False)