from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
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

    tahun = [
        "TINGKATAN SATU",
        "TINGKATAN DUA",
        "TINGKATAN TIGA",
        "TINGKATAN EMPAT",
        "TINGKATAN LIMA",
    ]
    kelas = ["AKIK", "BAIDURI", "DELIMA", "JED", "NILAM"]

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
            print(f"Processed page {p} - {q}")

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

    return jsonify(
        {
            "username": username,
            "password": password,
            "year": year,
            "message": student_data_message,
        }
    )


if __name__ == "__main__":
    app.run(port=5000)
