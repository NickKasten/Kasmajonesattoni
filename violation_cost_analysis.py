import pandas as pd
import os
import glob
import re
import numpy as np

# Step 1: Load the Payroll and Management data
payroll_mgmt_df = pd.read_csv('/Users/teddyjones/projects/Datathon/Kasmajonesattoni/Payroll_and_management.csv')

# Step 2: Process violation data 
# Option A: Load the combined violations file instead of individual files
try:
    all_violations_df = pd.read_csv('/Users/teddyjones/projects/Datathon/Kasmajonesattoni/Time Rates - violations.csv')
    print(f"Loaded violations data with {len(all_violations_df)} records")
    
    # Group by employee_id and year
    violation_summary = all_violations_df.groupby(['employee_id', 'year']).agg({
        'violations': 'sum'
    }).reset_index()
    
except Exception as e:
    print(f"Error loading violations file: {e}")
    
    # Option B: Try to process individual files with corrected ID extraction
    violations_data = []
    employee_files = glob.glob('employee_data/employee_*.csv')
    
    for file_path in employee_files:
        try:
            emp_df = pd.read_csv(file_path)
            
            # Extract employee_id from filename using regex to get just the number
            match = re.search(r'employee_(\d+)\.csv', file_path)
            if match:
                employee_id = int(match.group(1))
                
                # Group by year and sum violations
                yearly_violations = emp_df.groupby('year').agg({
                    'violations': 'sum'
                }).reset_index()
                
                # Add employee_id to the grouped data
                yearly_violations['employee_id'] = employee_id
                violations_data.append(yearly_violations)
            else:
                print(f"Couldn't extract employee ID from: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Combine all violation data
    if violations_data:
        violation_summary = pd.concat(violations_data)
        print(f"Processed violations for {len(violations_data)} employees")
    else:
        print("No violation data could be processed from individual files")
        exit(1)

# Step 3: Merge violation data with payroll and department info
merged_df = pd.merge(
    violation_summary,
    payroll_mgmt_df,
    on=['employee_id', 'year'],
    how='left'
)

# Step 4: Calculate violation costs
# California meal break penalty is typically one hour of pay per violation
merged_df['pay_rate'] = pd.to_numeric(merged_df['pay_rate'], errors='coerce')
merged_df['violation_cost'] = merged_df['violations'] * merged_df['pay_rate']

# Fill missing department/manager with "Unknown"
merged_df['department'] = merged_df['department'].fillna('Unknown')
merged_df['Supervisor'] = merged_df['Supervisor'].fillna('Unknown')

# Step 5: Calculate summary statistics
total_violations = merged_df['violations'].sum()
total_cost = merged_df['violation_cost'].sum()

# Department summaries
dept_summary = merged_df.groupby('department').agg({
    'violations': 'sum',
    'violation_cost': 'sum',
    'employee_id': pd.Series.nunique
}).reset_index()
dept_summary.columns = ['Department', 'Total Violations', 'Total Cost ($)', 'Number of Employees']
dept_summary['Avg Violations per Employee'] = dept_summary['Total Violations'] / dept_summary['Number of Employees']
dept_summary['Avg Cost per Employee ($)'] = dept_summary['Total Cost ($)'] / dept_summary['Number of Employees']
dept_summary = dept_summary.sort_values('Total Cost ($)', ascending=False)

# Manager summaries
mgr_summary = merged_df.groupby('Supervisor').agg({
    'violations': 'sum',
    'violation_cost': 'sum',
    'employee_id': pd.Series.nunique
}).reset_index()
mgr_summary.columns = ['Manager', 'Total Violations', 'Total Cost ($)', 'Number of Employees']
mgr_summary['Avg Violations per Employee'] = mgr_summary['Total Violations'] / mgr_summary['Number of Employees']
mgr_summary['Avg Cost per Employee ($)'] = mgr_summary['Total Cost ($)'] / mgr_summary['Number of Employees']
mgr_summary = mgr_summary.sort_values('Total Cost ($)', ascending=False)

# Employee summaries (top violators)
emp_summary = merged_df.groupby('employee_id').agg({
    'violations': 'sum',
    'violation_cost': 'sum',
    'department': 'first',
    'Supervisor': 'first',
    'pay_rate': 'mean'
}).reset_index()
emp_summary.columns = ['Employee ID', 'Total Violations', 'Total Cost ($)', 'Department', 'Manager', 'Avg Pay Rate ($)']
emp_summary = emp_summary.sort_values('Total Cost ($)', ascending=False)

# Year-over-year analysis
year_summary = merged_df.groupby('year').agg({
    'violations': 'sum',
    'violation_cost': 'sum',
    'employee_id': pd.Series.nunique
}).reset_index()
year_summary.columns = ['Year', 'Total Violations', 'Total Cost ($)', 'Number of Employees']
year_summary['Avg Violations per Employee'] = year_summary['Total Violations'] / year_summary['Number of Employees']
year_summary = year_summary.sort_values('Year')

# Step 6: Save results to files
output_dir = 'violation_analysis'
os.makedirs(output_dir, exist_ok=True)

# Save detailed data
merged_df.to_csv(f'{output_dir}/detailed_violation_costs.csv', index=False)

# Save summaries
dept_summary.to_csv(f'{output_dir}/department_summary.csv', index=False)
mgr_summary.to_csv(f'{output_dir}/manager_summary.csv', index=False)
emp_summary.to_csv(f'{output_dir}/employee_summary.csv', index=False)
year_summary.to_csv(f'{output_dir}/year_summary.csv', index=False)

# Step 7: Print summary report
print("\n===== VIOLATION COST ANALYSIS =====")
print(f"Total violations: {total_violations}")
print(f"Total estimated cost: ${total_cost:.2f}")
print("\nTop 5 Departments by Violation Cost:")
print(dept_summary[['Department', 'Total Violations', 'Total Cost ($)', 'Number of Employees']].head(5).to_string(index=False))

print("\nTop 5 Managers by Violation Cost:")
print(mgr_summary[['Manager', 'Total Violations', 'Total Cost ($)', 'Number of Employees']].head(5).to_string(index=False))

print("\nTop 5 Employees by Violation Cost:")
print(emp_summary[['Employee ID', 'Total Violations', 'Total Cost ($)', 'Department', 'Manager']].head(5).to_string(index=False))

print("\nYear-over-Year Analysis:")
print(year_summary[['Year', 'Total Violations', 'Total Cost ($)', 'Avg Violations per Employee']].to_string(index=False))

print(f"\nDetailed results saved to {output_dir}/ directory")