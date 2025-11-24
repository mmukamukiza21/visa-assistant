from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Free API for country info
COUNTRY_API = "https://restcountries.com/v3.1/all"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/countries')
def get_countries():
    try:
        response = requests.get(COUNTRY_API, timeout=10)
        response.raise_for_status()
        countries = sorted([c['name']['common'] for c in response.json()])
        return jsonify(countries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/visa', methods=['POST'])
def visa_info():
    data = request.json
    passport_country = data.get('passport')
    destination_country = data.get('destination')

    # Fallback visa info
    info = {
        "passport": passport_country,
        "destination": destination_country,
        "required_documents": [
            "Valid passport",
            "Visa application form",
            "Passport-size photo",
            "Travel itinerary",
            "Proof of funds"
        ],
        "note": "Check the embassy website for exact visa requirements."
    }
    return jsonify(info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
