from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import requests as rqst
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
CORS(app)


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
def extract_student_data(session):
    student_url = "https://sepkm.com/e/data_murid.php"
    params_class = {"tingkatan": "", "kelas": ""}
    table = []
    row = []
    mod = 0

    # Testing purposes

    """ tahun = [
        "TINGKATAN SATU",
        "TINGKATAN DUA",
        "TINGKATAN TIGA",
        "TINGKATAN EMPAT",
        "TINGKATAN LIMA",
    ]
    kelas = ["AKIK", "BAIDURI", "DELIMA", "JED", "NILAM"] """

    tahun = [
        "TINGKATAN SATU",
    ]
    kelas = ["AKIK", "BAIDURI"]

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
    df_stud = pd.DataFrame(table, columns=row_headers)
    df_stud.to_csv("student_data.csv")
    return f"Produced student_data.csv."


# Function to extract PHQ9 data
def getPHQ9Data(table, tableBody):
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


def extract_phq9_data(session):
    phq_url = "https://sepkm.com/e/minda_sihat3.php?id=PHQ9"
    params_page = {"page": ""}

    # Testing purposes
    # page = [str(i) for i in range(1, 1001)]
    page = [str(i) for i in range(1, 3)]

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

        table = getPHQ9Data(table, tableBody)

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

    # Convert df to csv
    df_phq.to_csv("phq9_data.csv")
    return f"Produced phq9_data.csv."


@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    year = data.get("year")

    session = rqst.Session()

    if not login(session, username, password):
        return jsonify({"error": "Login failed"}), 401

    if not change_year(session, year):
        return jsonify({"error": "Year change failed"}), 400

    student_data_message = extract_student_data(session)
    phq9_data_message = extract_phq9_data(session)

    return jsonify(
        {
            "username": username,
            "password": password,
            "year": year,
            "message_student_data": student_data_message,
            "message_phq9_data": phq9_data_message,
        }
    )


if __name__ == "__main__":
    app.run(port=5000)
