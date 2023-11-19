import pandas as pd

df = pd.read_csv('vapro 830-930 & 930 1030 & 1030 1130.csv')  # Replace 'report.csv' with your actual file path

number_to_name = {
    #ext mapping here
}

df['From number'] = df['From number'].map(number_to_name)

grouped_data = df.groupby('From number').agg({
    'Call initiated': ['count', 'min', 'max'],  # Get count, earliest, and latest 'Call initiated' timestamps in each group
    'Call duration': 'sum'
}).reset_index()

grouped_data.columns = ['From Number', 'Total Calls', 'First Call Timestamp', 'Last Call Timestamp', 'Total Call Duration']

grouped_data['Total Call Duration (HH:MM:SS)'] = pd.to_timedelta(grouped_data['Total Call Duration'], unit='s')
grouped_data['Total Call Duration (HH:MM:SS)'] = grouped_data['Total Call Duration (HH:MM:SS)'].apply(
    lambda x: f"{x.days * 24 + x.seconds // 3600:02}:{(x.seconds // 60) % 60:02}:{x.seconds % 60:02}")

grouped_data = grouped_data.drop('Total Call Duration', axis=1)

grouped_data.to_csv('vapro_output.csv', index=False)

print("VAPRO REPORT DONE")
