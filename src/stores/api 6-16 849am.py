from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import numpy as np
import requests as rqst
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
CORS(app)


@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    year = data.get("year")

    # create session object
    session = rqst.Session()

    # send GET request to login page
    login_url = "https://sepkm.com/e/login/login.php"
    response = session.get(login_url)

    # prepare login data
    login_data = {
        "login": username,
        "password": password,
    }

    # send POST request to login form
    login_response = session.post(login_url, data=login_data)

    # check if login was successful
    if "DASHBOARD SEKOLAH" in login_response.text:
        print("Login successful")
    else:
        print("Login failed")

    # Initialization

    student_url = "https://sepkm.com/e/data_murid.php"
    semak_url = "https://sepkm.com/e/minda_sihat_semak.php"
    gad_url = "https://sepkm.com/e/minda_sihat3.php?id=GAD7"
    phq_url = "https://sepkm.com/e/minda_sihat3.php?id=PHQ9"

    params_page = {
        "page": "1",
    }

    page = [str(i) for i in range(1, 1001)]

    # Assuming you've just logged in and created a session as in your previous code...

    # Prepare the data for the year change request
    year_data = {
        "year": year,  # or whatever year you want to switch to
    }

    # "2023 & 2024" is identified by year: 2023

    # Send the request
    year_url = (
        "https://sepkm.com/e/year.php"  # I'm guessing at this URL based on the script
    )
    year_response = session.get(year_url, params=year_data)

    # Check the response
    if year_response.status_code == 200:
        print("Year change successful")
    else:
        print("Year change failed")

    # Data extraction

    params_class = {
        "tingkatan": "TINGKATAN SATU",
        "kelas": "DELIMA",
    }

    # Make this robust
    tahun = [
        "TINGKATAN SATU",
        "TINGKATAN DUA",
        "TINGKATAN TIGA",
        "TINGKATAN EMPAT",
        "TINGKATAN LIMA",
    ]
    kelas = ["AKIK", "BAIDURI", "DELIMA", "JED", "NILAM"]

    table = []  # Initialize table as an empty list
    row = []
    mod = 0

    for p in tahun:
        params_class["tingkatan"] = p
        for q in kelas:
            params_class["kelas"] = q

            response = session.get(student_url, params=params_class)
            soup = bs(response.content, "html.parser")

            tableBody = soup.tbody
            print(f"Processing page {p} - {q}")

            for x in tableBody.find_all("td"):
                row.append(x.text)
                mod = mod + 1
                if mod % 6 == 0:
                    row.append(params_class["tingkatan"])
                    row.append(params_class["kelas"])
                    table.append(row)
                    row = []

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

    print(df_stud)

    df_stud.to_csv("student_data.csv")

    return jsonify({"username": username, "password": password, "year": year})


if __name__ == "__main__":
    app.run(port=5000)
