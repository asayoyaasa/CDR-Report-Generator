import pandas as pd

df = pd.read_csv('vapro 830-930 & 930 1030 & 1030 1130.csv')  # Replace 'report.csv' with your actual file path

number_to_name = {
    "DOMINIC HUNT": "0064*001",
    "CAROL TAN": "0064*002",
    "GEORGE KRUGER": "0064*003",
    "CHARLIE TAN": "0064*004",
    "ANNA YOUNG": "0064*005",
    "CAROLINE ROSE": "0064*006",
    "EDGAR LOU": "0064*007",
    "ANNA YOUNG 2": "0064*008",
    "LOGAN PARK": "0064*010",
    "TQ TRAINING 2": "0064*012",
    "EMILY PARK": "0064*013",
    "DANNY LIM": "0064*014",
    "DARREN LEE": "0064*015",
    "ARTHUR GARCIA": "0064*017",
    "KATE DHILLON": "0064*018",
    "LEWIS NAVARO": "0064*051",
    "HANNA KIM": "0064*052",
    "JESSICA HUDSON": "0064*053",
    "JAIMIE LYNN": "0064*055",
    "BRYAN LIEM": "0064*057",
    "SOFIA KIM": "0064*066",
    "LT 2": "0064*077",
    "JACOB FOX": "0064*103",
    "JACKSON FURRY": "0064*104",
    "KYLIE PARK": "0064*105",
    "ALLAN LOU": "0064*106",
    "GIA WATTS": "0064*108",
    "JOHN D'SOUZA": "0064*109",
    "ADNAN TAMZ": "0064*123",
    "NANDA TAMZ": "0064*170",
    "TRENING 1": "0064*201",
    "ROGER LEE": "0064*202",
    "JAMES SILVA": "0064*203",
    "TRENING 3": "0064*204",
    "WILLIAM LEE": "0064*205",
    "TRENING 5": "0064*206",
    "LUCY WOO": "0064*222",
    "TEST": "0064*323",
    "NEW": "0064*333",
    "DATAMINER": "0064*555",
    "NEW TQ LT 1": "0064*665",
    "IT DEPT": "0064*666",
    "IT DEPT2": "0064*667",
    "randee": "0064*668",
    "hendra": "0064*669",
    "Randee TEst": "0064*686",
    "MR.RANDEE": "0064*700",
    "RANDEE BP": "0064*701",
    "asa": "0064*777",
    "MIA HUNT": "0064*990",
    "MIA HUNTSWELL": "0064*991",
    "999": "0064*999"
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
