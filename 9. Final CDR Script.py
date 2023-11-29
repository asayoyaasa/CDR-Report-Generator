import os
import pandas as pd
import subprocess

# Common start and end time for all scripts
start_time = '2023-11-30 00:01:00'
end_time = '2023-11-30 02:00:59'

# File paths
file_path_3cx = '3cx.csv'
file_path_pbx = 'pbx.csv'
file_path_vapro = 'vapro.csv'

# Output file names
output_file_3cx = 'x3cx.csv'
output_file_pbx = 'xau.csv'
output_file_vapro = 'xvapro.csv'

# Check if 3cx.csv exists
if not os.path.exists(file_path_3cx):
    # If 3cx.csv does not exist, run the 3cx_combiner.py script
    subprocess.run(["python", "2.3cx_combiner.py"])
    print("3cx_combiner.py script executed")

# Check if 3cx.csv exists
if os.path.exists(file_path_3cx):
    # Check if the first column in the first row is 'Call Time'
    first_row = pd.read_csv(file_path_3cx, nrows=1, header=None)
    
    if first_row.iloc[0, 0] != 'Call Time':
        # If the first column is not 'Call Time', delete the first 4 rows and the last 2 rows
        df_3cx_temp = pd.read_csv(file_path_3cx, skiprows=range(0, 4), header=None)
        df_3cx_temp = df_3cx_temp.iloc[:-2]
        df_3cx_temp.to_csv(file_path_3cx, index=False, header=False)
        print("Deleted first 4 rows and last 2 rows in 3cx.csv")

# Mapping for 3CX
caller_id_mapping = {
    
    # Add other mappings as needed
}

# Mapping for PBX. For clarity this is #0001<<extension number 
cnam_mapping = {
    
    # Add other mappings as needed
}

# Mapping for VAPRO
number_to_name = {
    # Add other mappings as needed

# Check if 3cx.csv exists
if os.path.exists(file_path_3cx):
    # Script 1 - 3CX Report
    df_3cx = pd.read_csv(file_path_3cx)
    df_3cx['Talking'] = pd.to_timedelta(df_3cx['Talking'], errors='coerce')
    df_3cx['Call Time'] = pd.to_datetime(df_3cx['Call Time'])
    filtered_df_3cx = df_3cx[(df_3cx['Call Time'] >= start_time) & (df_3cx['Call Time'] <= end_time)]
    filtered_df_3cx = filtered_df_3cx[filtered_df_3cx['Destination'].astype(str).apply(len) == 11]
    filtered_df_3cx['Caller ID'] = filtered_df_3cx['Caller ID'].map(caller_id_mapping)
    grouped_data_3cx = filtered_df_3cx.groupby('Caller ID').agg({
        'Destination': 'count',
        'Talking': 'sum',
        'Call Time': ['min', 'max']
    }).reset_index()
    grouped_data_3cx.columns = ['Caller ID', 'Total Calls', 'Total Talking Time', 'First Call Time', 'Last Call Time']
    grouped_data_3cx['Total Talking Time'] = grouped_data_3cx['Total Talking Time'].apply(
        lambda x: f"{x.components.hours:02}:{x.components.minutes:02}:{x.components.seconds:02}")
    grouped_data_3cx.to_csv(output_file_3cx, index=False)
    print("3CX REPORT DONE")

    # Script 2 - PBX Report
    df_pbx = pd.read_csv(file_path_pbx)
    df_pbx['calldate'] = pd.to_datetime(df_pbx['calldate'])
    df_pbx['cnam'] = df_pbx['cnam'].map(cnam_mapping)
    filtered_df_pbx = df_pbx[(df_pbx['calldate'] >= start_time) & (df_pbx['calldate'] <= end_time)]
    filtered_df_pbx = filtered_df_pbx[filtered_df_pbx['dst'].astype(str).apply(len) == 11]
    grouped_data_pbx = filtered_df_pbx.groupby('cnam').agg({
        'dst': 'count',
        'billsec': 'sum',
        'calldate': ['min', 'max']
    }).reset_index()
    grouped_data_pbx.columns = ['Caller Name', 'Total Calls', 'Total Billsec (HH:MM:SS)', 'First Call Timestamp', 'Last Call Timestamp']
    grouped_data_pbx['Total Billsec (HH:MM:SS)'] = pd.to_timedelta(grouped_data_pbx['Total Billsec (HH:MM:SS)'], unit='s')
    grouped_data_pbx['Total Billsec (HH:MM:SS)'] = grouped_data_pbx['Total Billsec (HH:MM:SS)'].apply(
        lambda x: f"{x.days * 24 + x.seconds // 3600:02}:{(x.seconds // 60) % 60:02}:{x.seconds % 60:02}")

    # Check if 'Total Billsec' column exists before dropping
    if 'Total Billsec' in grouped_data_pbx.columns:
        grouped_data_pbx = grouped_data_pbx.drop('Total Billsec', axis=1)  # Drop 'Total Billsec' column

    grouped_data_pbx.to_csv(output_file_pbx, index=False)
    print("PBX REPORT DONE")

    # Script 3 - VAPRO Report
    df_vapro = pd.read_csv(file_path_vapro)
    df_vapro['From number'] = df_vapro['From number'].map(number_to_name)
    df_vapro['Call initiated'] = pd.to_datetime(df_vapro['Call initiated'])
    filtered_df_vapro = df_vapro[(df_vapro['Call initiated'] >= start_time) & (df_vapro['Call initiated'] <= end_time)]
    filtered_df_vapro = filtered_df_vapro[filtered_df_vapro['To number'].astype(str).apply(len) == 11]
    grouped_data_vapro = filtered_df_vapro.groupby('From number').agg({
        'Call initiated': ['count', 'min', 'max'],
        'Call duration': 'sum'
    }).reset_index()
    grouped_data_vapro.columns = ['From Number', 'Total Calls', 'First Call Timestamp', 'Last Call Timestamp', 'Total Call Duration (HH:MM:SS)']
    grouped_data_vapro['Total Call Duration (HH:MM:SS)'] = pd.to_timedelta(grouped_data_vapro['Total Call Duration (HH:MM:SS)'], unit='s')
    grouped_data_vapro['Total Call Duration (HH:MM:SS)'] = grouped_data_vapro['Total Call Duration (HH:MM:SS)'].apply(
        lambda x: f"{x.days * 24 + x.seconds // 3600:02}:{(x.seconds // 60) % 60:02}:{x.seconds % 60:02}")
    grouped_data_vapro.to_csv(output_file_vapro, index=False)
    print("VAPRO REPORT DONE")

# Run the combined.py script
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
print("Combined script executed")
