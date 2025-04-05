from sqlalchemy import create_engine
from sqlalchemy import URL
import Config
import pandas as pd

    
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_HOST = Config.MYSQL_HOST
MYSQL_PORT = Config.MYSQL_PORT
MYSQL_DATABASE = Config.MYSQL_DATABASE

#make connection string and create engine 
url_object = URL.create(
    "mysql+pymysql",
    username=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    database=MYSQL_DATABASE,
)
engine = create_engine(url_object, echo=False)

#Convert CSV to pandas df

file_names = ["sample_payroll.csv", "sample_timekeeping.csv"]
df_list = []

for file in file_names:
    df = pd.read_csv(file, na_values=['', 'NA', 'NaN'])
    df_list.append(df)


#Put the df into the MySQL db with df.to_sql

for i in range(len(file_names)):
    file = file_names[i]

    table_name = file[:len(file) - 4]

    df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
    print("Added table to db")