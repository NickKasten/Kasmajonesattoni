import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for better-looking plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

# Create output directory for visualizations
viz_dir = 'violation_visualizations'
os.makedirs(viz_dir, exist_ok=True)

print("Loading violation analysis data...")

# Load the data files
dept_df = pd.read_csv('violation_analysis/department_summary.csv')
mgr_df = pd.read_csv('violation_analysis/manager_summary.csv')
emp_df = pd.read_csv('violation_analysis/employee_summary.csv')
year_df = pd.read_csv('violation_analysis/year_summary.csv')
detailed_df = pd.read_csv('violation_analysis/detailed_violation_costs.csv')

# 1. Year-over-Year Analysis
plt.figure(figsize=(12, 6))
ax = sns.barplot(x='Year', y='Total Violations', data=year_df, palette='Blues_d')
plt.title('Meal Break Violations by Year', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Number of Violations', fontsize=14)

# Add value labels on bars
for i, v in enumerate(year_df['Total Violations']):
    ax.text(i, v + 50, f"{int(v)}", ha='center', fontsize=12)
    
# Add trend line
plt.plot(year_df['Year'], year_df['Total Violations'], 'ro-', linewidth=2)

# Add average violations per employee as a line on secondary axis
ax2 = ax.twinx()
ax2.plot(year_df['Year'], year_df['Avg Violations per Employee'], 'g^-', linewidth=2)
ax2.set_ylabel('Avg Violations per Employee', fontsize=14, color='g')
ax2.tick_params(axis='y', colors='g')

plt.tight_layout()
plt.savefig(f'{viz_dir}/violations_by_year.png', dpi=300)

# 2. Department Analysis
# Sort departments by total cost
dept_df_sorted = dept_df.sort_values('Total Cost ($)', ascending=False)

plt.figure(figsize=(14, 8))
ax = sns.barplot(x='Department', y='Total Cost ($)', data=dept_df_sorted, palette='viridis')
plt.title('Cost of Meal Break Violations by Department', fontsize=16)
plt.xlabel('Department', fontsize=14)
plt.ylabel('Total Cost ($)', fontsize=14)
plt.xticks(rotation=45, ha='right')

# Add value labels
for i, v in enumerate(dept_df_sorted['Total Cost ($)']):
    ax.text(i, v + 500, f"${int(v):,}", ha='center', fontsize=10)

# Add number of violations as text
for i, (cost, violations) in enumerate(zip(dept_df_sorted['Total Cost ($)'], dept_df_sorted['Total Violations'])):
    ax.text(i, cost/2, f"{int(violations)} violations", ha='center', color='white', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{viz_dir}/cost_by_department.png', dpi=300)

# 3. Top Managers
# Filter for managers with at least 2 employees to focus on meaningful comparisons
top_mgrs = mgr_df[mgr_df['Number of Employees'] >= 2].sort_values('Avg Cost per Employee ($)', ascending=False).head(10)

plt.figure(figsize=(14, 8))
ax = sns.barplot(x='Manager', y='Avg Cost per Employee ($)', data=top_mgrs, palette='magma')
plt.title('Average Violation Cost per Employee by Manager (Managers with 2+ Employees)', fontsize=16)
plt.xlabel('Manager', fontsize=14)
plt.ylabel('Avg Cost per Employee ($)', fontsize=14)
plt.xticks(rotation=45, ha='right')

# Add employee count labels
for i, (cost, emps) in enumerate(zip(top_mgrs['Avg Cost per Employee ($)'], top_mgrs['Number of Employees'])):
    ax.text(i, cost + 200, f"{int(emps)} employees", ha='center', fontsize=10)
    ax.text(i, cost/2, f"${int(cost)}", ha='center', color='white', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{viz_dir}/cost_per_employee_by_manager.png', dpi=300)

# 4. Top 10 Employees with Most Violations
top_emps = emp_df.sort_values('Total Violations', ascending=False).head(10)

plt.figure(figsize=(14, 8))
# Create a custom palette that colors bars by department
dept_colors = dict(zip(top_emps['Department'].unique(), 
                       sns.color_palette("Set2", len(top_emps['Department'].unique()))))
bar_colors = [dept_colors[dept] for dept in top_emps['Department']]

ax = sns.barplot(x='Employee ID', y='Total Violations', data=top_emps, palette=bar_colors)
plt.title('Top 10 Employees with Most Meal Break Violations', fontsize=16)
plt.xlabel('Employee ID', fontsize=14)
plt.ylabel('Number of Violations', fontsize=14)

# Add department and cost labels
for i, (emp, dept, cost) in enumerate(zip(top_emps['Employee ID'], top_emps['Department'], top_emps['Total Cost ($)'])):
    ax.text(i, top_emps['Total Violations'].iloc[i] + 5, f"${int(cost)}", ha='center', fontsize=9)
    ax.text(i, top_emps['Total Violations'].iloc[i]/2, dept, ha='center', color='white', 
            fontsize=8, fontweight='bold', rotation=90)

# Add a legend for departments
handles = [plt.Rectangle((0,0),1,1, color=dept_colors[dept]) for dept in dept_colors]
plt.legend(handles, dept_colors.keys(), title="Department", loc='upper right')

plt.tight_layout()
plt.savefig(f'{viz_dir}/top_employees_by_violations.png', dpi=300)

# 5. Scatter plot of Pay Rate vs. Violations
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(x='Avg Pay Rate ($)', y='Total Violations', 
                         hue='Department', size='Total Cost ($)',
                         sizes=(50, 500), alpha=0.7, data=emp_df)
plt.title('Relationship Between Pay Rate and Number of Violations', fontsize=16)
plt.xlabel('Average Pay Rate ($)', fontsize=14)
plt.ylabel('Number of Violations', fontsize=14)

# Add employee IDs for top violators
for i, row in emp_df.sort_values('Total Violations', ascending=False).head(5).iterrows():
    plt.annotate(f"ID: {row['Employee ID']}", 
                xy=(row['Avg Pay Rate ($)'], row['Total Violations']),
                xytext=(5, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig(f'{viz_dir}/pay_rate_vs_violations.png', dpi=300)

# 6. Heatmap of violations by department and year
# Prepare data for heatmap
dept_year_data = detailed_df.groupby(['department', 'year']).agg({'violations': 'sum'}).reset_index()
dept_year_pivot = dept_year_data.pivot(index='department', columns='year', values='violations').fillna(0)

plt.figure(figsize=(12, 10))
ax = sns.heatmap(dept_year_pivot, annot=True, fmt='.0f', cmap='YlOrRd', 
            linewidths=0.5, cbar_kws={'label': 'Number of Violations'})
plt.title('Violations Heatmap by Department and Year', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Department', fontsize=14)
plt.tight_layout()
plt.savefig(f'{viz_dir}/dept_year_heatmap.png', dpi=300)

# 7. Pie Chart of Total Violation Costs by Department (Top 5)
top_5_depts = dept_df.sort_values('Total Cost ($)', ascending=False).head(5)
other_cost = dept_df.sort_values('Total Cost ($)', ascending=False).iloc[5:]['Total Cost ($)'].sum()

plt.figure(figsize=(10, 10))
data = list(top_5_depts['Total Cost ($)']) + [other_cost]
labels = list(top_5_depts['Department']) + ['Other Departments']
colors = sns.color_palette('Spectral', len(data))

plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, 
        wedgeprops={'edgecolor': 'white', 'linewidth': 1})
plt.axis('equal')
plt.title('Distribution of Violation Costs by Department', fontsize=16)
plt.tight_layout()
plt.savefig(f'{viz_dir}/cost_distribution_pie.png', dpi=300)

# 8. Compliance Improvement: Violations per Employee Year-over-Year
plt.figure(figsize=(12, 6))
ax = sns.lineplot(x='Year', y='Avg Violations per Employee', 
                 data=year_df, marker='o', linewidth=3, markersize=10)
plt.title('Compliance Improvement: Avg Violations per Employee', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Average Violations per Employee', fontsize=14)
plt.grid(True, linestyle='--')
plt.ylim(bottom=0)

# Add percentage change annotations
for i in range(1, len(year_df)):
    current = year_df['Avg Violations per Employee'].iloc[i]
    previous = year_df['Avg Violations per Employee'].iloc[i-1]
    pct_change = ((current - previous) / previous) * 100
    color = 'green' if pct_change < 0 else 'red'
    plt.annotate(f"{pct_change:.1f}%", 
                xy=(year_df['Year'].iloc[i], current),
                xytext=(0, 10), textcoords='offset points',
                ha='center', color=color, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{viz_dir}/compliance_improvement.png', dpi=300)

# 9. Bar chart showing violation trends for top 5 departments
top_5_dept_names = dept_df.sort_values('Total Cost ($)', ascending=False).head(5)['Department'].tolist()
dept_trends = detailed_df[detailed_df['department'].isin(top_5_dept_names)]
dept_year_trends = dept_trends.groupby(['department', 'year']).agg({'violations': 'sum'}).reset_index()

plt.figure(figsize=(14, 8))
ax = sns.barplot(x='year', y='violations', hue='department', data=dept_year_trends, palette='Set2')
plt.title('Violation Trends for Top 5 Departments', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Number of Violations', fontsize=14)
plt.legend(title='Department')
plt.tight_layout()
plt.savefig(f'{viz_dir}/dept_violation_trends.png', dpi=300)

print(f"All visualizations saved to {viz_dir}/ directory")