import pandas as pd

# Load the new CSV file into a pandas DataFrame
df = pd.read_csv('3cx.csv')  # Replace '3cx.csv' with your actual file path

# Convert 'Talking' column to timedelta format
df['Talking'] = pd.to_timedelta(df['Talking'], errors='coerce')

# Convert 'Call Time' column to datetime format
df['Call Time'] = pd.to_datetime(df['Call Time'])

# Define the specific timeline
start_time = '2023-11-14 08:30:00'
end_time = '2023-11-14 09:30:00'

# Filter the data based on the specific timeline
filtered_df = df[(df['Call Time'] >= start_time) & (df['Call Time'] <= end_time)]

# Group the filtered data by 'Caller ID' and calculate the count of 'Destination', the sum of 'Talking',
# the earliest 'Call Time', and the latest 'Call Time' in each group
grouped_data = filtered_df.groupby('Caller ID').agg({
    'Destination': 'count',          # Count the occurrences of 'Destination'
    'Talking': 'sum',                # Sum the 'Talking' durations
    'Call Time': ['min', 'max']      # Get both the earliest and latest 'Call Time' timestamps in each group
}).reset_index()  # Reset the index to make 'Caller ID' a regular column

# Rename the columns for clarity
grouped_data.columns = ['Caller ID', 'Total Calls', 'Total Talking Time', 'First Call Time', 'Last Call Time']

# Convert the 'Total Talking Time' sum to HH:MM:SS format
grouped_data['Total Talking Time'] = grouped_data['Total Talking Time'].apply(
    lambda x: f"{x.components.hours:02}:{x.components.minutes:02}:{x.components.seconds:02}")

# Save the grouped data to a new CSV file
grouped_data.to_csv('3cxv2out_filtered.csv', index=False)

print("3CX REPORT DONE")  # Print a message indicating that the report is done
