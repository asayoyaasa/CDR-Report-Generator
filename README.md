# README for Script 8.0. (only need to run this one)

## 3CX, PBX, and VAPRO Report Generator

This Python script is designed to generate reports from three different CSV files (`3cx.csv`, `pbx.csv`, and `vapro.csv`). The reports provide insights into call data, including total calls, total talking time, and timestamps of the first and last calls within a specified time range.

### Prerequisites
- Ensure that the required CSV files (`3cx.csv`, `pbx.csv`, and `vapro.csv`) are present in the script's working directory.
- Python environment with the necessary dependencies (pandas) installed.

### Customizable Settings
- **Time Range:** The start and end times for the reports are set as `start_time` and `end_time` variables at the beginning of the script. Adjust these values according to the desired time range.

### How to Run
1. Place the three input CSV files (`3cx.csv`, `pbx.csv`, and `vapro.csv`) in the script's working directory.
2. Execute the script in a Python environment.

### Output
- The script generates three separate reports: `x3cx.csv`, `xau.csv`, and `xvapro.csv`.

### Customization
#### 3CX Mapping
- The `caller_id_mapping` dictionary can be customized to map specific caller IDs to desired names.

#### PBX Mapping
- The `cnam_mapping` dictionary can be customized to map specific names to caller IDs.

#### VAPRO Mapping
- The `number_to_name` dictionary can be customized to map specific numbers to caller names.

# README for Script 8.1.

## CSV File Combiner and Cleaner

This Python script combines and cleans data from two CSV files (`carlos3cx.csv` and `va3cx.csv`). The cleaned data is then saved to a new CSV file (`3cx.csv`).

### How to Run
1. Place the input CSV files (`carlos3cx.csv` and `va3cx.csv`) in the script's working directory.
2. Execute the script in a Python environment.

### Output
- The script generates a combined and cleaned CSV file named `3cx.csv`.

# README for Script 8.2.

## Combined Report Formatter

This Python script reads data from three CSV files (`x3cx.csv`, `xau.csv`, and `xvapro.csv`) and combines them into a single, formatted CSV file (`combined_output.csv`). The script also aggregates and cleans the data, ensuring accurate and comprehensive reporting.

### Prerequisites
- Ensure that the required CSV files (`x3cx.csv`, `xau.csv`, and `xvapro.csv`) are present in the script's working directory.
- Python environment with the necessary dependencies (pandas) installed.

### How to Run
1. Place the three input CSV files in the script's working directory.
2. Execute the script in a Python environment.

### Output
- The script generates a combined and formatted CSV file named `combined_output.csv`.

### Customization
- The script provides flexibility in customizing the output format, including mapping, aggregation, and timestamp adjustments.

---


