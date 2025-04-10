import pandas as pd
import datetime
import seaborn as sns
import matplotlib.pyplot as plt

file_names = ["sample_payroll.csv", "sample_timekeeping.csv"]

df_list = []

for file in file_names:
    df = pd.read_csv(file, na_values=['', 'NA', 'NaN'])
    df_list.append(df)

# df.fillna()

# 

# Determining Break Length

def getBreakLengths(df):
    # Convert the columns to datetime
    df["punchin2"] = pd.to_datetime(df["punchin2"], errors='coerce')
    df["punchout1"] = pd.to_datetime(df["punchout1"], errors='coerce')
    df["punchin3"] = pd.to_datetime(df["punchin3"], errors='coerce')
    df["punchout2"] = pd.to_datetime(df["punchout2"], errors='coerce')
    df["date"] = pd.to_datetime(df["date"], errors='coerce')
    
    # Create a new DataFrame to store break lengths
    new_df = pd.DataFrame()
    new_df["employee_id"] = df["employee_id"]
    new_df["date"] = df["date"]
    
    # Calculate break_length_1: difference between punchin2 and punchout1
    new_df["break_length_1"] = df["punchin2"] - df["punchout1"]
    
    # Calculate break_length_2 only if punchin3 is not null
    new_df["break_length_2"] = df["punchin3"] - df["punchout2"]
    
    # Write the new DataFrame to a CSV file
    new_df.to_csv("break_lengths.csv", index=False)
    print("CSV created successfully!")

def getHoursWorked(df):

   # Convert the columns to datetime
    df["punchin1"] = pd.to_datetime(df["punchin1"], errors='coerce')
    df["punchout1"] = pd.to_datetime(df["punchout1"], errors='coerce')
    df["punchin2"] = pd.to_datetime(df["punchin2"], errors='coerce')
    df["punchout2"] = pd.to_datetime(df["punchout2"], errors='coerce')
    df["punchin3"] = pd.to_datetime(df["punchin3"], errors='coerce')
    df["punchout3"] = pd.to_datetime(df["punchout3"], errors='coerce')
    df["date"] = pd.to_datetime(df["date"], errors='coerce')

    new_df = pd.DataFrame()
    new_df["employee_id"] = df["employee_id"]
    new_df["date"] = df["date"]

    period1 = (df["punchout1"] - df["punchin1"]).fillna(pd.Timedelta(0))
    period2 = (df["punchout2"] - df["punchin2"]).fillna(pd.Timedelta(0))
    period3 = (df["punchout3"] - df["punchin3"]).fillna(pd.Timedelta(0))

    # Sum the timedeltas for total work time
    total_work = period1 + period2 + period3

    # Convert the total timedelta to hours (as a decimal)
    new_df["hours_worked"] = total_work.dt.total_seconds() / 3600

    new_df["hours_worked"] = new_df["hours_worked"].round(1)

    # Save the result to a CSV file
    new_df.to_csv("hours_worked.csv", index=False)

    print("CSV of hours worked created")

getBreakLengths(df_list[1])
getHoursWorked(df_list[1])

"""
# Heat map (Shows how correlated each feature is)
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()
"""
