import pandas as pd

# Read the CSV file
df = pd.read_csv('pbx.csv')  # Replace 'ca pbx.csv' with your actual file path

# Group the data by 'cnam' and calculate the count of 'dst' and the sum of 'billsec' along with the earliest and latest 'calldate' timestamps in each group
grouped_data = df.groupby('cnam').agg({
    'dst': 'count',
    'billsec': 'sum',
    'calldate': ['min', 'max']  # Get the earliest and latest 'calldate' timestamps in each group
}).reset_index()

# Renaming the columns to avoid tuple naming
grouped_data.columns = ['Caller Name', 'Total Calls', 'Total Billsec', 'First Call Timestamp', 'Last Call Timestamp']

# Convert the "Total Billsec" from seconds to HH:MM:SS format
grouped_data['Total Billsec (HH:MM:SS)'] = pd.to_timedelta(grouped_data['Total Billsec'], unit='s')
grouped_data['Total Billsec (HH:MM:SS)'] = grouped_data['Total Billsec (HH:MM:SS)'].apply(lambda x: f"{x.days * 24 + x.seconds // 3600:02}:{(x.seconds // 60) % 60:02}:{x.seconds % 60:02}")

# Drop the original "Total Billsec" column
grouped_data = grouped_data.drop('Total Billsec', axis=1)

# Save the grouped data to a new CSV file
grouped_data.to_csv('au_pbx_output.csv', index=False)

print("PBX REPORT DONE")
