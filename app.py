import requests
from datetime import datetime
from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def home():

	weather = None



	if request.method == "POST": 

		city = request.form["city"]

		print("User searched for:", city)

		url = "https://geocoding-api.open-meteo.com/v1/search"

		params = {
				"name": city,
				"count": 1,
				"language": "en",
				"format": "json"
			}

		try:
			response = requests.get(url, params = params)
			response.raise_for_status()
			data = response.json()
		except requests.RequestException:
			return render_template(
				"index.html",
				error="Could not connect to the weather service"
			)

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

		weather_icons = {
    		0: "☀️",
    		1: "🌤",
    		2: "⛅",
    		3: "☁️",
    		61: "🌧",
    		63: "🌧",
    		65: "⛈"
		}

		try:
			weather_response = requests.get(weather_url, params=weather_params)

			weather_response.raise_for_status()

			weather_data = weather_response.json()

		except requests.RequestException:
			return render_template("index.html", error="Could not connect to the weather service")

		current = weather_data["current"]

		weather_code = current["weather_code"]

		daily = weather_data["daily"]

		dates = weather_data["daily"]

		dates = daily["time"]
		max_temperatures = daily["temperature_2m_max"]
		min_temperatures = daily["temperature_2m_min"]
		weather_codes = daily["weather_code"]

		forecast = []

		for i in range(5):

			date = datetime.strptime(dates[i], "%Y-%m-%d")

			day = date.strftime("%A")
			month = date.strftime("%B")
			day_number = date.strftime("%d")

			condition = weather_conditions.get(weather_codes[i], "Unknown")

			forecast.append({
				"day": day,
				"month": month,
				"day_number": day_number,
				"condition": condition,
				"max_temperature": max_temperatures[i],
				"min_temperature": min_temperatures[i],
				"condition": condition,
				"icon": weather_icons.get(weather_codes[i], "❓")
			})
			
		weather_icon = weather_icons.get(weather_code, "❓")

		weather = {
			"city": result["name"],
			"country": result["country"],
			"temperature": current["temperature_2m"],
			"humidity": current["relative_humidity_2m"],
			"wind": current["wind_speed_10m"],
			"condition": condition,
			"icon": weather_icon,
			"day": forecast[0]["day"],
    		"month": forecast[0]["month"],
    		"day_number": forecast[0]["day_number"]
		}

		weather_code = current["weather_code"]

		condition = weather_conditions.get(weather_code, "Unknown")

		print("\n" + "="*50)
		print("CURRENT WEATHER")
		print("="*50)
		print(f"City:        {weather['city']}, {weather['country']}")
		print(f"Temperature: {weather['temperature']}°C")
		print(f"Humidity:    {weather['humidity']}%")
		print(f"Wind:        {weather['wind']} km/h")
		print(f"Condition:   {weather['condition']}")

		print("\n" + "="*50)
		print("5-DAY FORECAST")
		print("="*50)

		for day in forecast:
			print(f"{day['day']:<10} {day['day_number']} {day['month']:<10} "f"{day['condition']:<15} {day['min_temperature']}°C - {day['max_temperature']}°C")

		print("="*50 + "\n")

		return render_template(
			"index.html",
			weather = weather,
			forecast = forecast
		)

	return render_template("index.html", weather=None, forecast=None, error=None)

if __name__ == "__main__":
	app.run(debug=True)
