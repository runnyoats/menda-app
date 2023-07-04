import pandas as pd
from sqlalchemy import create_engine

# Creating connection to the database
engine = create_engine("mysql+pymysql://root:trachel@127.0.0.1:3306/menda_02")

# Reading data from the table
df = pd.read_sql("SELECT * FROM students", con=engine)

# Writing data to an Excel file
df.to_excel("students_data.xlsx", index=False)
