import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def home():

	weather = None

	if request.method == "POST": 

		city = request.form["city"]

		print("User sezrched for:", city)

		url = "https://geocoding-api.open-meteo.com/v1/search"

		params = {
				"name": city,
				"count": 1,
				"language": "en",
				"format": "json"
			}

		response = requests.get(url, params = params)
		data = response.json()

		if "results" not in data:
			return render_template(
				"index.html",
				error="City not found"
			)

		result = data["results"][0]

		latitude = result["latitude"]
		longitude = result["longitude"]

		weather_url = "https://api.open-meteo.com/v1/forecast"

		weather_params = {
    		"latitude": latitude,
    		"longitude": longitude,

    		"current": [
        		"temperature_2m",
				"apparent_temperature",
        		"relative_humidity_2m",
        		"wind_speed_10m",
				"weather_code"
        	],

			"daily": [
				"weather_code",
				"temperature_2m_max",
				"temperature_2m_min",
			],

			"forecast_days": 5,

			"timezone": "auto"
		}

		weather_conditions = {
    		0: "Sunny",
    		1: "Mainly clear",
    		2: "Partly cloudy",
    		3: "Overcast",
    		61: "Rain",
    		63: "Rain",
    		65: "Heavy rain"
		}

		weather_code = current["weather_code"]

		condition = weather_conditions.get(weather_code, "Unknown")

		weather_response = requests.get(weather_url, params=weather_params)

		weather_data = weather_response.json()

		current = weather_data["current"]

		daily = weather_data["daily"]
		
		weather = {
			"city": result["name"],
			"country": result["country"],
			"temperature": current["temperature_2m"],
			"humidity": current["relative_humidity_2m"],
			"wind": current["wind_speed_10m"],
			"wind": current["wind_speed_10m"],
			"condition": condition
		}

		return render_template(
			"index.html",
			weather = weather 
		)

	return render_template("index.html ")


if __name__ == "__main__":
	app.run(debug=True)
