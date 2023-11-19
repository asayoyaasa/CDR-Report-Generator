import os
import pandas as pd
import subprocess

# Common start and end time for all scripts
start_time = '2023-11-16 21:30:00'
end_time = '2023-11-17 14:30:00'

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
    subprocess.run(["python", "3cx_combiner.py"])
    print("3cx_combiner.py script executed")

# Mapping for 3CX
caller_id_mapping = {
    "ARTHUR GARCIA 2 FANVIL-X4 (112)": "ARTHUR GARCIA",
    "GEORGE KRUGER HUNTERS (115)": "MATT GUNNER",
    "JACKSON FURY HUNTERS (116)": "JACKSON FURY",
    "JACOB FOX 2 FANVIL X4U (114)": "JACOB FOX",
    "JOHN D'SOUZA (102)": "JOHN D'SOUZA",
    "LEWIS NAVARO HUNTERS (124)": "LEWIS NAVARO",
    "MICHAEL HANSON (106)": "JASON SPARK",
    "SOFIA KIM (104)": "SOFIA KIM"
    # Add other mappings as needed
}

# Mapping for PBX. For clarity this is #0001<<extension number 
cnam_mapping = {
    "DOMINIC HUNT":    "DOMINIC HUNT",           #0001
    "JACOB FOX":       "JACOB FOX",              #0002
    "ARTHUR GARCIA":   "ARTHUR GARCIA",          #0003
    "MIA HUNT":        "MIA HUNT",               #0004
    "EDGAR LOU":       "EDGAR LOU",              #0005
    "CAROL TAN":       "CAROL TAN",              #0006
    "MATT GUNNER":     "MATT GUNNER",            #0007
    "JACKSON FURY":    "JACKSON FURY",           #0008
    "LEWIS NAVARO":    "LEWIS NAVARO",           #0009
    "JOHN D'SOUZA":    "JOHN D'SOUZA",           #0010
    "KATE DHILLON":    "NO USER KATE DHILLON",   #0011
    "BRYAN LIEM":      "NO USER BRYAN LIEM",     #0012
    "IT SUPPORT - EDDY": "IT SUPPORT - EDDY",    #0013
    "ALLAN LOU":       "NO USER ALLAN LOU",      #0014
    "JASON SPARK":     "JASON SPARK",            #0015
    "CAROLINE ROSE":   "CAROL LYNN ROSE",        #0021
    "SOFIA KIM":       "SOFIA KIM",              #0022
    "ANNA YOUNG":      "ANNA YOUNG",             #0023
    "OLIVER WILLIAMS": "OLIVER WILLIAMS",        #0024
    "EMILY PARK":      "EMILY PARK",             #0025
    "NATHAN LEE":      "LOGAN PARK",             #0026
    "USER 27":         "NO USER USER 27",        #0027
    "JAIMIE LYNN":     "JAIMIE LYNN",            #0031
    "KYLIE PARK":      "NO USER KYLIE PARK",     #0032
    "HANNA KIM":       "NO USER HANNA KIM",      #0033
    "DANZEL WEI":      "DANNY LIM",              #0034
    "IT - NANDA":      "NO USER IT - NANDA",     #0035
    "ALEX TAN":        "GIA WATTS",              #0036
    "CHARLIE TAN":     "NO USER CHARLIE TAN",    #0037
    "ROGER LEE":       "ROGER LEE",              #0038
    "USER-0039":       "NO USER USER-0039",      #0039
    "WILLIAM LEE":     "WILLIAM LEE",            #0040
    "DANIEL TAN":      "NO USER DANIEL TAN",     #0041
    "JAMES SILVA":     "JAMES SILVA",            #0042
    "IT SUPPORT":      "IT SUPPORT",             #0666
    "777":             "777",                    #0777
    "asa":             "asa",                    #1234
    "Mia":             "Mia",                    #9999


    # Add other mappings as needed
}

# Mapping for VAPRO
number_to_name = {
    "0064*008": "ANNA YOUNG",
    "0064*777": "ASA",
    "0064*555": "DATAMINER",
    "0064*669": "HENDRA",
    "0064*123": "ADNAN",
    "0064*170": "NANDA",
    "0064*333": "IT1",
    "0064*323": "IT2",
    "0064*666": "IT3",
    "0064*667": "IT4",
    "0064*203": "JAMES SILVA",
    "0064*004": "CHARLIE TAN",
    "0064*202": "ROGER LEE",
    "0064*006": "CAROL LYNN ROSE",
    "0064*052": "HANNA KIM",
    "0064*103": "JACOB FOX",
    "0064*990": "MIA HUNT",
    "0064*012": "NEW TQ 012",
    "0064*665": "NEW TQ 665",
    "0064*013": "EMILY PARK",
    "0064*077": "NEW TQ 077",
    "0064*108": "GIA WATTS",
    "0064*106": "ALLAN LOU",
    "0064*017": "ARTHUR GARCIA",
    "0064*002": "CAROL TAN",
    "0064*015": "JASON SPARK",
    "0064*001": "DOMINIC HUNT",
    "0064*003": "MATT GUNNER",
    "0064*104": "JACKSON FURY",
    "0064*109": "JOHN D'SOUZA",
    "0064*018": "GIA WATTS",
    "0064*051": "LEWIS NAVARO",
    "0064*991": "MIA HUNT",
    "0064*010": "LOGAN PARK",
    "0064*066": "SOFIA KIM",
    "0064*005": "ANNA YOUNG",
    "0064*057": "BRYAN LIEM",
    "0064*014": "DANNY LIM",
    "0064*007": "EDGAR LOU",
    "0064*055": "JAIMIE LYNN",
    "0064*053": "OLIVER WILLIAMS",
    "0064*105": "KYLIE PARK",
    "0064*222": "LUCY WOO",
    "0064*700": "MR.RANDEE",
    "0064*668": "randee",
    "0064*701": "RANDEE BP",
    "0064*686": "Randee TEst",
    "0064*201": "TRENING 1",
    "0064*204": "TRENING 3",
    "0064*205": "WILLIAM LEE",
    "0064*206": "TRENING 5",
    "0064*999": "USER - 999",
}

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
    subprocess.run(["python", "v14.1.py"])
    print("v14.1.py script executed")

