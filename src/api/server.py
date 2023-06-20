from flask import Flask, request, jsonify
from flask_cors import CORS
from sepkm_scraper import (
    sepkm_scraper,
)  # assuming sepkm_scraper.py is in the same directory
from murid_data import (
    get_murid_data,
)

app = Flask(__name__)
CORS(app)


@app.route("/murid_data", methods=["GET"])
def students():
    data = get_murid_data()
    return jsonify(data)


@app.route("/sepkm_scraper", methods=["POST"])
def scrape_sepkm():
    data = request.get_json()
    response = sepkm_scraper(
        data.get("username"), data.get("password"), data.get("year")
    )
    if "error" in response:
        return jsonify(response), response.get("status", 400)
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=5000)
