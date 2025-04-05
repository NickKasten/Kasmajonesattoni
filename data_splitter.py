import pandas as pd
import os

# Create output directory if it doesn't exist
output_dir = "employee_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the CSV file
csv_path = "Time Rates - violations.csv"
df = pd.read_csv(csv_path)

# Drop empty rows (if needed)
df = df.dropna(how='all')

# Group by employee_id and save separate files
for employee_id, group in df.groupby('employee_id'):
    output_file = os.path.join(output_dir, f"employee_{employee_id}.csv")
    group.to_csv(output_file, index=False)
    print(f"Created file for employee {employee_id}: {output_file}")

print(f"Finished splitting data for {len(df['employee_id'].unique())} employees")