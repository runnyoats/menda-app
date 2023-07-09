import pandas as pd
import numpy as np
import requests as rqst
from bs4 import BeautifulSoup as bs
import os

script_path = os.path.realpath(__file__)

(dirname, filename) = os.path.split(script_path)


# Function to log into the site
def login(session, username, password):
    login_url = "https://sepkm.com/e/login/login.php"
    login_data = {"login": username, "password": password}
    login_response = session.post(login_url, data=login_data)
    return "DASHBOARD SEKOLAH" in login_response.text


# Function to change the year
def change_year(session, year):
    year_data = {"year": year}
    year_url = "https://sepkm.com/e/year.php"
    year_response = session.get(year_url, params=year_data)
    return year_response.status_code == 200


# Function to extract data
def extract_students(session):
    student_url = "https://sepkm.com/e/data_murid.php"
    params_class = {"tingkatan": "", "kelas": ""}
    table = []
    row = []
    mod = 0

    tahun = [
        "TINGKATAN SATU",
        "TINGKATAN DUA",
        "TINGKATAN TIGA",
        "TINGKATAN EMPAT",
        "TINGKATAN LIMA",
    ]
    kelas = ["AKIK", "BAIDURI", "DELIMA", "JED", "NILAM"]

    # Testing purposes
    # tahun = [
    #     "TINGKATAN SATU",
    # ]
    # kelas = ["AKIK", "BAIDURI"]

    for p in tahun:
        params_class["tingkatan"] = p
        for q in kelas:
            params_class["kelas"] = q
            response = session.get(student_url, params=params_class)
            soup = bs(response.content, "html.parser")
            tableBody = soup.tbody
            for x in tableBody.find_all("td"):
                row.append(x.text)
                mod = mod + 1
                if mod % 6 == 0:
                    row.append(params_class["tingkatan"])
                    row.append(params_class["kelas"])
                    table.append(row)
                    row = []
            print(f"Processing Student page {p} - {q}")

    row_headers = [
        "bil",
        "nama",
        "kp",
        "sijil_lahir",
        "tarikh_lahir",
        "alamat",
        "tingkatan",
        "kelas",
    ]
    df_students = pd.DataFrame(table, columns=row_headers)
    # df_students.to_csv(os.path.join(dirname, "tmp/scraped_students_semiraw.csv"))
    return df_students


# Function to extract table data for PHQ9 & GAD7
def get_table_data(table, tableBody):
    for trTag in tableBody.find_all("tr", {"bgcolor": "#b3ffec"}):
        for tdTag in trTag.find_all("td"):
            table.append(tdTag.text)

        for selectTag in trTag.find_all("select"):
            selectBool = 0
            tempOption = "text"
            for optionTag in selectTag.find_all("option"):
                if optionTag.has_attr("selected"):
                    selectBool = 1
                    tempOption = optionTag
                    break

            # Append a value, either the selected value or 0
            if selectBool == 0:
                table.append("0")
            else:
                table.append(tempOption.text)

        for thTag in trTag.find_all("th", {"width": "10%"}):
            table.append(thTag.text)

    return table


# Function to extract table data for SEMAK
def get_semak_data(table, tableBody):
    for trTag in tableBody.find_all("tr", {"bgcolor": "#b3ffec"}):
        for tdTag in trTag.find_all("td"):
            table.append(tdTag.text)

        for thTag in trTag.find_all("th", {"width": "10%"}):
            table.append(thTag.text)

        for selectTag in trTag.find_all("select"):
            selectBool = 0
            tempOption = "text"
            for optionTag in selectTag.find_all("option"):
                if optionTag.has_attr("selected"):
                    selectBool = 1
                    tempOption = optionTag
                    break

            # Append a value, either the selected value or 0
            if selectBool == 0:
                table.append("0")
            else:
                table.append(tempOption.text)

    return table


def extract_phq9(session):
    phq_url = "https://sepkm.com/e/minda_sihat3.php?id=PHQ9"
    params_page = {"page": ""}

    # Testing purposes
    # page = [str(i) for i in range(1, 3)]
    page = [str(i) for i in range(1, 1001)]

    table = []
    for p in page:
        params_page["page"] = p
        response = session.get(phq_url, params=params_page)
        soup = bs(response.content, features="lxml")
        tableBody = soup.tbody
        print(f"Processing PHQ-9 page {p}")

        # If tbody is effectively empty, break the loop
        if not tableBody or not tableBody.text.strip():
            break

        table = get_table_data(table, tableBody)

    # Reshape and print
    npTable = np.array(table).reshape(-1, 16)

    # Convert to dataframe
    row_headers = [
        "no",
        "nama",
        "kelas",
        "phq_1",
        "phq_2",
        "phq_3",
        "phq_4",
        "phq_5",
        "phq_6",
        "phq_7",
        "phq_8",
        "phq_9",
        "phq_tarikh",
        "phq_jumlah",
        "phq_krisis",
        "phq_intervensi",
    ]
    df_phq = pd.DataFrame(npTable, columns=row_headers)

    # Data cleaning
    df_phq = df_phq.drop(columns=["no"])
    df_phq["phq_tarikh"] = df_phq["phq_tarikh"].str.replace("\n", "")
    df_phq["phq_tarikh"] = df_phq["phq_tarikh"].str.replace(" ", "")
    # df_phq.to_csv(os.path.join(dirname, "tmp/scraped_phq9_data.csv"))

    return df_phq


def extract_gad7(session):
    gad_url = "https://sepkm.com/e/minda_sihat3.php?id=GAD7"
    params_page = {"page": ""}

    # Testing purposes
    # page = [str(i) for i in range(1, 3)]
    page = [str(i) for i in range(1, 1001)]

    table = []
    for p in page:
        params_page["page"] = p
        response = session.get(gad_url, params=params_page)
        soup = bs(response.content, features="lxml")
        tableBody = soup.tbody
        print(f"Processing GAD-7 page {p}")

        # If tbody is effectively empty, break the loop
        if not tableBody or not tableBody.text.strip():
            break

        table = get_table_data(table, tableBody)

    # Reshape and print
    npTable = np.array(table).reshape(-1, 14)

    # Convert to dataframe
    row_headers = [
        "no",
        "nama",
        "kelas",
        "gad_1",
        "gad_2",
        "gad_3",
        "gad_4",
        "gad_5",
        "gad_6",
        "gad_7",
        "gad_tarikh",
        "gad_jumlah",
        "krisis",
        "gad_intervensi",
    ]
    df_gad = pd.DataFrame(npTable, columns=row_headers)

    # Data cleaning
    df_gad = df_gad.drop(columns=["no", "krisis"])
    df_gad["gad_tarikh"] = df_gad["gad_tarikh"].str.replace("\n", "")
    df_gad["gad_tarikh"] = df_gad["gad_tarikh"].str.replace(" ", "")
    # df_gad.to_csv(os.path.join(dirname, "tmp/scraped_gad7_data.csv"))

    return df_gad


def extract_semak(session):
    semak_url = "https://sepkm.com/e/minda_sihat_semak.php"
    params_page = {"page": ""}

    # Testing purposes
    # page = [str(i) for i in range(1, 3)]
    page = [str(i) for i in range(1, 1001)]

    table = []
    for p in page:
        params_page["page"] = p
        response = session.get(semak_url, params=params_page)
        soup = bs(response.content, features="lxml")
        tableBody = soup.tbody
        print(f"Processing SEMAK page {p}")

        # If tbody is effectively empty, break the loop
        if not tableBody or not tableBody.text.strip():
            break

        table = get_semak_data(table, tableBody)

    # Reshape and print
    npTable = np.array(table).reshape(-1, 29)

    # Convert to dataframe
    row_headers = [
        "no",
        "nama",
        "kelas",
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
    df_semak = pd.DataFrame(npTable, columns=row_headers)

    # Data cleaning
    df_semak = df_semak.drop(columns=["no"])
    df_semak["semak_tarikh"] = df_semak["semak_tarikh"].str.replace("\n", "")
    df_semak["semak_tarikh"] = df_semak["semak_tarikh"].str.replace(" ", "")
    # df_semak.to_csv(os.path.join(dirname, "tmp/scraped_semak_data.csv"))

    return df_semak


def process_csv_files(year, df_gad, df_phq, df_semak, df_students):
    print(f"Processing data")

    # Unneeded column
    df_students = df_students.drop(
        ["bil", "sijil_lahir", "alamat", "tingkatan", "kelas"], axis=1
    )

    # Create 'jantina' column based on 'kp' values
    df_students["jantina"] = df_students["kp"].apply(
        lambda x: "L" if int(str(x)[-1]) % 2 == 1 else "P"
    )

    # Convert date columns to datetime
    df_students["tarikh_lahir"] = pd.to_datetime(
        df_students["tarikh_lahir"], format="%d-%m-%Y"
    )

    # Convert date format to yyyy-mm-dd
    df_students["tarikh_lahir"] = df_students["tarikh_lahir"].dt.strftime("%Y-%m-%d")

    # Merge dataframes based on 'nama' column
    merged_df = (
        df_students.merge(df_semak, on="nama")
        .merge(df_phq, on="nama")
        .merge(df_gad, on="nama")
    ).copy()

    # Drop duplicate class columns
    merged_df = merged_df.drop(
        ["nama", "tarikh_lahir", "jantina", "kelas_x", "kelas_y"], axis=1
    ).copy()

    # Add 'sidang' column (according to year data chosen to extract from SePKM)
    merged_df["sidang"] = year

    # Convert date columns to datetime
    merged_df["phq_tarikh"] = pd.to_datetime(merged_df["phq_tarikh"], format="%d-%m-%Y")
    merged_df["gad_tarikh"] = pd.to_datetime(merged_df["gad_tarikh"], format="%d-%m-%Y")
    merged_df["semak_tarikh"] = pd.to_datetime(
        merged_df["semak_tarikh"], format="%d-%m-%Y"
    )

    # Convert date format to yyyy-mm-dd
    merged_df["phq_tarikh"] = merged_df["phq_tarikh"].dt.strftime("%Y-%m-%d")
    merged_df["gad_tarikh"] = merged_df["gad_tarikh"].dt.strftime("%Y-%m-%d")
    merged_df["semak_tarikh"] = merged_df["semak_tarikh"].dt.strftime("%Y-%m-%d")

    # Extract 'tingkatan' from 'kelas'
    merged_df["tingkatan"] = merged_df["kelas"].str.extract(r"T(\d+)-")
    merged_df["tingkatan"] = merged_df["tingkatan"].astype(int)

    # Extract 'kelas' after the '-' character
    merged_df["kelas"] = merged_df["kelas"].str.split("-", expand=True)[1]

    # Convert 'merged_df' to the desired column order
    desired_order = ["kp", "sidang", "tingkatan", "kelas"]
    phq_columns = [
        col
        for col in merged_df.columns
        if col.startswith("phq_") and col != "phq_tarikh"
    ]
    gad_columns = [
        col
        for col in merged_df.columns
        if col.startswith("gad_") and col != "gad_tarikh"
    ]
    semak_columns = [
        col
        for col in merged_df.columns
        if col.startswith("semak_") and col != "semak_tarikh"
    ]

    new_columns = (
        desired_order
        + phq_columns
        + ["phq_tarikh"]
        + gad_columns
        + ["gad_tarikh"]
        + semak_columns
        + ["semak_tarikh"]
    )

    df_submissions = merged_df[new_columns]

    # Conversion for checking if necessary
    df_students.to_csv(os.path.join(dirname, "tmp/scraped_students.csv"))
    df_submissions.to_csv(os.path.join(dirname, "tmp/scraped_submissions.csv"))

    return df_students, df_submissions


def append_to_database(df_students, df_submissions):
    from sqlalchemy import create_engine

    # Import file into database
    print(f"Updating database")
    engine = create_engine("mysql+pymysql://root:trachel@127.0.0.1:3306/menda_02")
    df_students.to_sql("students", con=engine, index=False, if_exists="append")
    df_submissions.to_sql("submissions", con=engine, index=False, if_exists="append")


def sepkm_scraper(username, password, year):
    session = rqst.Session()

    if not login(session, username, password):
        return {"error": "Login failed"}, 401

    if not change_year(session, year):
        return {"error": "Year change failed"}, 400

    df_students = extract_students(session)
    df_phq9 = extract_phq9(session)
    df_gad7 = extract_gad7(session)
    df_semak = extract_semak(session)

    df_students, df_submissions = process_csv_files(
        year, df_gad7, df_phq9, df_semak, df_students
    )

    append_to_database(df_students, df_submissions)

    return {
        "username": username,
        "password": password,
        "year": year,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scraper for SEPKM")
    parser.add_argument("username", type=str, help="Username for SEPKM")
    parser.add_argument("password", type=str, help="Password for SEPKM")
    parser.add_argument("year", type=int, help="Year for data scraping")
    args = parser.parse_args()

    result = sepkm_scraper(args.username, args.password, args.year)
    print(result)
