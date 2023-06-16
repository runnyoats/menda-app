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

    return jsonify({"username": username, "password": password, "year": year})


if __name__ == "__main__":
    app.run(port=5000)
