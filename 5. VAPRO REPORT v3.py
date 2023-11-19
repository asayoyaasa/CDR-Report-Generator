import pandas as pd

df = pd.read_csv('vapro 830-930 & 930 1030 & 1030 1130.csv')  # Replace 'vapro.csv' with your actual file path

number_to_name = {
    #ext mapping here
}

df['From number'] = df['From number'].map(number_to_name)

# Convert 'Call initiated' column to datetime format
df['Call initiated'] = pd.to_datetime(df['Call initiated'])

# Define the specific timeline
start_time = '2023-11-14 08:30:00'
end_time = '2023-11-14 09:30:00'

# Filter the data based on the specific timeline
filtered_df = df[(df['Call initiated'] >= start_time) & (df['Call initiated'] <= end_time)]

# Group the filtered data by 'From number' and calculate the count, earliest, and latest 'Call initiated' timestamps, and the sum of 'Call duration' in each group
grouped_data = filtered_df.groupby('From number').agg({
    'Call initiated': ['count', 'min', 'max'],
    'Call duration': 'sum'
}).reset_index()

grouped_data.columns = ['From Number', 'Total Calls', 'First Call Timestamp', 'Last Call Timestamp', 'Total Call Duration']

grouped_data['Total Call Duration (HH:MM:SS)'] = pd.to_timedelta(grouped_data['Total Call Duration'], unit='s')
grouped_data['Total Call Duration (HH:MM:SS)'] = grouped_data['Total Call Duration (HH:MM:SS)'].apply(
    lambda x: f"{x.days * 24 + x.seconds // 3600:02}:{(x.seconds // 60) % 60:02}:{x.seconds % 60:02}")

grouped_data = grouped_data.drop('Total Call Duration', axis=1)

grouped_data.to_csv('vapro_output_830930.csv', index=False)

print("VAPRO REPORT DONE")
