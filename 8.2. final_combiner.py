import pandas as pd

# Read data from CSV files
df_3cx = pd.read_csv('x3cx.csv')
df_pbx = pd.read_csv('xau.csv')
df_vapro = pd.read_csv('xvapro.csv')

# Reorder and select columns for each dataframe
df_3cx = df_3cx[['Caller ID', 'Total Calls', 'Total Talking Time', 'First Call Time', 'Last Call Time']]
df_pbx = df_pbx[['Caller Name', 'Total Calls', 'Total Billsec (HH:MM:SS)', 'First Call Timestamp', 'Last Call Timestamp']]
df_vapro = df_vapro[['From Number', 'Total Calls', 'Total Call Duration (HH:MM:SS)', 'First Call Timestamp', 'Last Call Timestamp']]

# Rename columns to match the desired output
df_pbx.columns = ['Caller ID', 'Total Calls', 'Total Talking Time', 'First Call Time', 'Last Call Time']
df_vapro.columns = ['Caller ID', 'Total Calls', 'Total Talking Time', 'First Call Time', 'Last Call Time']

# Concatenate dataframes
combined_df = pd.concat([df_3cx, df_vapro, df_pbx], ignore_index=True)

# Convert 'Total Talking Time' to timedelta and sum for duplicate 'Caller ID'
combined_df['Total Talking Time'] = pd.to_timedelta(combined_df['Total Talking Time']).groupby(combined_df['Caller ID']).transform('sum')

# Combine 'Total Calls' for duplicate 'Caller ID'
combined_df['Total Calls'] = combined_df.groupby('Caller ID')['Total Calls'].transform('sum')

# Format 'Total Talking Time' to HH:MM:SS
combined_df['Total Talking Time'] = combined_df['Total Talking Time'].apply(lambda x: str(x).split()[-1])

# Aggregate 'First Call Time' and 'Last Call Time' based on your requirements
combined_df['First Call Time'] = combined_df.groupby('Caller ID')['First Call Time'].transform('min')
combined_df['Last Call Time'] = combined_df.groupby('Caller ID')['Last Call Time'].transform('max')

# Drop duplicate 'Caller ID' entries
combined_df = combined_df.drop_duplicates(subset='Caller ID')

# Sort the dataframe based on 'Caller ID'
combined_df = combined_df.sort_values(by='Caller ID').reset_index(drop=True)

# Save the combined dataframe to a CSV file
combined_df.to_csv('combined_output.csv', index=False)

# Print the combined dataframe
print(combined_df)
