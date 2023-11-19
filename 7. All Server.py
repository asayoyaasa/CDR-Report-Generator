import pandas as pd

# Common start and end time for all scripts
start_time = '2023-11-15 21:30:00'
end_time = '2023-11-16 14:30:00'

# File paths
file_path_3cx = '3cx.csv'
file_path_pbx = 'pbx.csv'
file_path_vapro = 'vapro.csv'

# Output file names
output_file_3cx = 'x3cx.csv'
output_file_pbx = 'xau.csv'
output_file_vapro = 'xvapro.csv'

# Script 1 - 3CX Report
df_3cx = pd.read_csv(file_path_3cx)
df_3cx['Talking'] = pd.to_timedelta(df_3cx['Talking'], errors='coerce')
df_3cx['Call Time'] = pd.to_datetime(df_3cx['Call Time'])
filtered_df_3cx = df_3cx[(df_3cx['Call Time'] >= start_time) & (df_3cx['Call Time'] <= end_time)]
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
filtered_df_pbx = df_pbx[(df_pbx['calldate'] >= start_time) & (df_pbx['calldate'] <= end_time)]
grouped_data_pbx = filtered_df_pbx.groupby('cnam').agg({
    'dst': 'count',
    'billsec': 'sum',
    'calldate': ['min', 'max']
}).reset_index()
grouped_data_pbx.columns = ['Caller Name', 'Total Calls', 'Total Billsec', 'First Call Timestamp', 'Last Call Timestamp']
grouped_data_pbx['Total Billsec (HH:MM:SS)'] = pd.to_timedelta(grouped_data_pbx['Total Billsec'], unit='s')
grouped_data_pbx['Total Billsec (HH:MM:SS)'] = grouped_data_pbx['Total Billsec (HH:MM:SS)'].apply(
    lambda x: f"{x.days * 24 + x.seconds // 3600:02}:{(x.seconds // 60) % 60:02}:{x.seconds % 60:02}")
grouped_data_pbx.to_csv(output_file_pbx, index=False)
print("PBX REPORT DONE")

# Script 3 - VAPRO Report
df_vapro = pd.read_csv(file_path_vapro)
number_to_name = {
    #ext mapping here
}
df_vapro['From number'] = df_vapro['From number'].map(number_to_name)
df_vapro['Call initiated'] = pd.to_datetime(df_vapro['Call initiated'])
filtered_df_vapro = df_vapro[(df_vapro['Call initiated'] >= start_time) & (df_vapro['Call initiated'] <= end_time)]
grouped_data_vapro = filtered_df_vapro.groupby('From number').agg({
    'Call initiated': ['count', 'min', 'max'],
    'Call duration': 'sum'
}).reset_index()
grouped_data_vapro.columns = ['From Number', 'Total Calls', 'First Call Timestamp', 'Last Call Timestamp', 'Total Call Duration']
grouped_data_vapro['Total Call Duration (HH:MM:SS)'] = pd.to_timedelta(grouped_data_vapro['Total Call Duration'], unit='s')
grouped_data_vapro['Total Call Duration (HH:MM:SS)'] = grouped_data_vapro['Total Call Duration (HH:MM:SS)'].apply(
    lambda x: f"{x.days * 24 + x.seconds // 3600:02}:{(x.seconds // 60) % 60:02}:{x.seconds % 60:02}")
grouped_data_vapro = grouped_data_vapro.drop('Total Call Duration', axis=1)
grouped_data_vapro.to_csv(output_file_vapro, index=False)
print("VAPRO REPORT DONE")
