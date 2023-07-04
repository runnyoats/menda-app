import pandas as pd
from sqlalchemy import create_engine
import sys

### Dropping existing rows ###
import pymysql

# Establish database connection
conn = pymysql.connect(
    db="menda_04",
    user="root",
    password="trachel",
    host="127.0.0.1",
    port=3306,
)

# Create a cursor object
cur = conn.cursor()

# Execute the SQL commands to delete all rows from the tables
cur.execute("DELETE FROM submissions;")
cur.execute("DELETE FROM students;")

# Commit the transactions
conn.commit()

# Close the cursor and the connection
cur.close()
conn.close()

### Processing & importing user file

# Accept the file path as a command-line argument
file_path = sys.argv[1]

# Create connection to the database
engine = create_engine("mysql+pymysql://root:trachel@127.0.0.1:3306/menda_04")

# Read Excel file into DataFrame
df = pd.read_excel(file_path)

# Specify column names for students and submissions
students_columns = ["nama", "kp", "tarikh_lahir", "jantina"]
submissions_columns = [
    "kp",
    "sidang",
    "tingkatan",
    "kelas",
    "phq_tarikh",
    "phq_1",
    "phq_2",
    "phq_3",
    "phq_4",
    "phq_5",
    "phq_6",
    "phq_7",
    "phq_8",
    "phq_9",
    "phq_jumlah",
    "phq_krisis",
    "phq_intervensi",
    "gad_tarikh",
    "gad_1",
    "gad_2",
    "gad_3",
    "gad_4",
    "gad_5",
    "gad_6",
    "gad_7",
    "gad_jumlah",
    "gad_intervensi",
    "semak_tarikh",
    "semak_1",
    "semak_2",
    "semak_3",
    "semak_4",
    "semak_5",
    "semak_6",
    "semak_7",
    "semak_8",
    "semak_9",
    "semak_10",
    "semak_11",
    "semak_12",
    "semak_13",
    "semak_14",
    "semak_15",
    "semak_16",
    "semak_17",
    "semak_18",
    "semak_19",
    "semak_20",
    "semak_21",
    "semak_22",
    "semak_23",
    "semak_24",
    "semak_25",
]

# Split df into df_students and df_submissions
df_students = df[students_columns].copy()
df_submissions = df[submissions_columns]

# Remove duplicates from df_students based on 'kp'
df_students.drop_duplicates(subset=["kp"], keep="first", inplace=True)

# Write DataFrame to the 'students' and 'submissions' tables
# Be careful with this - make sure to backup your data

df_students.to_sql("students", con=engine, index=False, if_exists="append")
df_submissions.to_sql("submissions", con=engine, index=False, if_exists="append")
