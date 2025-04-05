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
    data = {}        

    #Get the difference in time bewteeen punchOut1 and punchIn2 and for now make a new file called break_lengths.csv with employeeID, data, breakLengths

    for line in df:
        data["employee_id"] = df["employee_id"]
        data["date"] = df["date"]

        break_length_1 = df["punchin2"] - df["punchout1"]

        if df["punchin3"] is not nul
    

# Heat map (Shows how correlated each feature is)
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

