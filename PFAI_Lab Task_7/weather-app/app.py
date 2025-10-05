from flask import Flask, render_template, request
import os, requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_weather(city: str, units: str = "metric"):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": units}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

@app.route("/", methods=["GET", "POST"])
def index():
    weather, error = None, None
    units = request.form.get("units", "metric")

    if request.method == "POST":
        city = (request.form.get("city") or "").strip()

        if not API_KEY:
            error = "Missing API key. Add it to .env as OPENWEATHER_API_KEY."
        elif not city:
            error = "Please enter a city."
        else:
            try:
                data = fetch_weather(city, units)
                weather = {
                    "city": f"{data['name']}, {data['sys'].get('country','')}",
                    "desc": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"],
                    "temp": round(data["main"]["temp"]),
                    "feels": round(data["main"]["feels_like"]),
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"],
                    "units_symbol": "°C" if units == "metric" else "°F",
                    "units": units,
                }
            except requests.HTTPError as e:
                if e.response is not None and e.response.status_code == 404:
                    error = "City not found. Try another name."
                else:
                    error = f"Weather service error."
            except Exception:
                error = "Something went wrong. Please try again."

    return render_template("index.html", weather=weather, error=error, units=units)

if __name__ == "__main__":
    app.run(debug=True)
