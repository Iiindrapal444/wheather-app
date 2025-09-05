from flask import Flask, render_template, request
import requests
from config import API_KEY, BASE_URL


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }
            response = requests.get(BASE_URL, params=params)

            print("DEBUG URL:", response.url)
            print("DEBUG STATUS:", response.status_code)
            print("DEBUG RESPONSE:", response.json())


            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"]
                }
            else:
                error = "City not found. Please try again."

    return render_template("index.html", weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
