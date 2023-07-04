import pandas as pd
from sqlalchemy import create_engine
import sys

# Accept the file path as a command-line argument
file_path = sys.argv[1]

# Create connection to the database
engine = create_engine("mysql+pymysql://root:trachel@127.0.0.1:3306/menda_02")

# Read Excel file into DataFrame
df = pd.read_excel(file_path)

print(df)

# Assuming the DataFrame has the same structure as the database tables,
# you could split it into two parts - one for each table
# Replace 'students_columns' and 'submissions_columns' with actual columns lists
# df_students = df[students_columns]
# df_submissions = df[submissions_columns]

# Write DataFrame to the 'students' and 'submissions' tables
# The if_exists='replace' will replace the existing table data with the new one
# Be careful with this option - make sure to backup your data
# df_students.to_sql("students", con=engine, index=False, if_exists="replace")
# df_submissions.to_sql("submissions", con=engine, index=False, if_exists="replace")
