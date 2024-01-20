import sys
import pandas as pd
from datetime import timedelta

def analyze_employee_data(file_path):
    try:
        # Read the Excel file
        df = pd.read_excel("C:\\Users\\vavil\\Downloads\\question.py")

        # Assuming the file has columns like 'Employee', 'Position', 'Date', 'Hours Worked'
        # Please adjust these column names based on your actual data

        # Sort the data by 'Employee' and 'Date'
        df.sort_values(by=['Employee', 'Date'], inplace=True)

        # Function to calculate consecutive days worked
        def consecutive_days(series):
            return (series - series.shift(1)).dt.days == 1

        # Function to check time between shifts
        def time_between_shifts(series):
            return ((series - series.shift(1)) < timedelta(hours=10)) & ((series - series.shift(1)) > timedelta(hours=1))

        # Function to check total hours worked in a single shift
        def total_hours_worked(series):
            return series.sum() > timedelta(hours=14)

        # Apply the conditions and filter the dataframe
        consecutive_days_mask = df.groupby('Employee')['Date'].transform(consecutive_days)
        between_shifts_mask = df.groupby('Employee')['Date'].transform(time_between_shifts)
        total_hours_mask = df.groupby('Employee')['Hours Worked'].transform(total_hours_worked)

        result_df = df[consecutive_days_mask | between_shifts_mask | total_hours_mask]

        # Print the results to console
        print(result_df[['Employee', 'Position']])

        # Save the results to output.txt
        result_df[['Employee', 'Position']].to_csv('output.txt', index=False)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/your/file.xlsx")
    else:
        file_path = sys.argv[1]
        analyze_employee_data(file_path)
