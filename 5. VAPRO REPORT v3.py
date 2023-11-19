import pandas as pd

df = pd.read_csv('vapro 830-930 & 930 1030 & 1030 1130.csv')  # Replace 'vapro.csv' with your actual file path

number_to_name = {
    "0064*001": "DOMINIC HUNT",
    "0064*002": "CAROL TAN",
    "0064*003": "GEORGE KRUGER",
    "0064*004": "CHARLIE TAN",
    "0064*005": "ANNA YOUNG",
    "0064*006": "GRACE TAN",
    "0064*007": "EDGAR LOU",
    "0064*008": "ANNA YOUNG",
    "0064*010": "LOGAN PARK",
    "0064*012": "NEW TQ 012",
    "0064*013": "EMILY PARK",
    "0064*014": "DANZEL WEI",
    "0064*015": "DARREN LEE",
    "0064*017": "ARTHUR GARCIA",
    "0064*018": "KATE DHILLON",
    "0064*051": "LEWIS NAVARO",
    "0064*052": "HANNA KIM",
    "0064*053": "JESSICA HUDSON",
    "0064*055": "JAIMIE LYNN",
    "0064*057": "BRYAN LIEM",
    "0064*066": "SOFIA KIM",
    "0064*077": "NEW TQ 077",
    "0064*103": "JACOB FOX",
    "0064*104": "JACKSON FURRY",
    "0064*105": "KYLIE PARK",
    "0064*106": "ALLAN LOU",
    "0064*108": "GIA WATTS",
    "0064*109": "JOHN D'SOUZA",
    "0064*123": "ADNAN",
    "0064*170": "NANDA",
    "0064*201": "TRENING 1",
    "0064*202": "DANNY LIM",
    "0064*203": "JAMES WANG",
    "0064*204": "TRENING 3",
    "0064*205": "WILLIAM LEE",
    "0064*206": "TRENING 5",
    "0064*222": "LUCY WOO",
    "0064*323": "IT2",
    "0064*333": "IT1",
    "0064*555": "DATAMINER",
    "0064*666": "IT3",
    "0064*667": "IT4",
    "0064*668": "randee",
    "0064*669": "HENDRA",
    "0064*686": "Randee TEst",
    "0064*700": "MR.RANDEE",
    "0064*701": "RANDEE BP",
    "0064*777": "ASA",
    "0064*990": "MIA HUNT",
    "0064*991": "MIA HUNTSWELL",
    "0064*999": "USER - 999"
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
