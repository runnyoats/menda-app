import pandas as pd
from sqlalchemy import create_engine

# Creating connection to the database
engine = create_engine("mysql+pymysql://root:trachel@127.0.0.1:3306/menda_02")

# Reading data from the tables
df_students = pd.read_sql("SELECT * FROM students", con=engine)
df_submissions = pd.read_sql("SELECT * FROM submissions", con=engine)

# Joining the tables on the 'kp' column
df_joined = pd.merge(df_students, df_submissions, on="kp", how="left")

# Drop unneeded column
df_joined.drop("submission_id", axis=1, inplace=True)

# Writing data to an Excel file
df_joined.to_excel("students_submissions_data.xlsx", index=False)
