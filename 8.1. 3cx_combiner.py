import pandas as pd

def combine_and_clean_csv(file1, file2, output_file):
    # Read CSV files, skipping specified rows
    df1 = pd.read_csv(file1, skiprows=range(5), skipfooter=2, engine='python', header=None)
    df2 = pd.read_csv(file2, skiprows=range(6), skipfooter=2, engine='python', header=None)

    # Combine the two dataframes
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Write the combined dataframe to a new CSV file
    combined_df.to_csv(output_file, index=False, header=False)

if __name__ == "__main__":
    # Input file names
    file1_name = "carlos3cx.csv"
    file2_name = "va3cx.csv"

    # Output file name
    output_file_name = "3cx.csv"

    # Combine and clean CSV files
    combine_and_clean_csv(file1_name, file2_name, output_file_name)

    print(f"Combined and cleaned data saved to {output_file_name}")
