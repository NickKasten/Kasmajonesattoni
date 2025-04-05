import pandas as pd
import os

# Read the datasets
payroll_df = pd.read_csv('/Users/teddyjones/projects/Datathon/Kasmajonesattoni/Payroll.csv')
timekeeping_df = pd.read_csv('/Users/teddyjones/projects/Datathon/Kasmajonesattoni/Timekeeping.csv')

# Extract unique department and supervisor for each employee
# Taking the most recent department and supervisor for each employee
employee_dept_manager = timekeeping_df.sort_values('date', ascending=False).drop_duplicates(
    subset=['employee_id'], keep='first')[['employee_id', 'department', 'Supervisor']]

# Merge payroll data with department and supervisor
result_df = pd.merge(
    payroll_df,
    employee_dept_manager,
    on='employee_id',
    how='left'  # Keep all payroll records, even if no matching timekeeping record
)

# Save to new CSV file
output_path = '/Users/teddyjones/projects/Datathon/Kasmajonesattoni/Payroll_and_management.csv'
result_df.to_csv(output_path, index=False)

print(f"Created {output_path} with {len(result_df)} rows")

# Show the first few rows of the new file
print("\nFirst few rows of the new file:")
print(result_df.head())

# Count employees missing department/supervisor information
missing_info = result_df[result_df['department'].isna()]['employee_id'].nunique()
print(f"\nEmployees with missing department/supervisor information: {missing_info}")