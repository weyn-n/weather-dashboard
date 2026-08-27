import requests
from datetime import datetime
from flask import Flask, render_template, request

# Create the Flask application
app = Flask(__name__)

# Handle both page loading (GET) and city searches (POST)
@app.route("/", methods=["GET", "POST"])

def home():

	weather = None

	if request.method == "POST": 

		# Get the city name submitted by the user
		city = request.form["city"]

		print("User searched for:", city)

		# Use the geocoding API to convert the city name into coordinates
		url = "https://geocoding-api.open-meteo.com/v1/search"

		params = {
				"name": city,
				"count": 1,
				"language": "en",
				"format": "json"
			}

		# Handle connection errors when the weather service is unavailable
		try:
			response = requests.get(url, params = params)
			response.raise_for_status()
			data = response.json()
		except requests.RequestException:
			return render_template(
				"index.html",
				error="Could not connect to the weather service"
			)

		# Check whether the API found the requested city
		if "results" not in data:
			return render_template(
				"index.html",
				error="City not found"
			)

		result = data["results"][0]

		# Check whether the API found the requested city
		latitude = result["latitude"]
		longitude = result["longitude"]

		# Request current weather and a five-day forecast
		weather_url = "https://api.open-meteo.com/v1/forecast"

		weather_params = {
    		"latitude": latitude,
    		"longitude": longitude,

    		"current": [
        		"temperature_2m",
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

		# Convert weather codes returned by the API into readable descriptions
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
		dates = daily["time"]

		max_temperatures = daily["temperature_2m_max"]
		min_temperatures = daily["temperature_2m_min"]
		weather_codes = daily["weather_code"]

		forecast = []

		# Build a user-friendly forecast for each of the five days
		for i in range(5):

			# Convert the API date string into separate day, month, and day number values
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
				"icon": weather_icons.get(weather_codes[i], "❓")
			})
			
		weather_icon = weather_icons.get(weather_code, "❓")

		# Convert the API date string into separate day, month, and day number values
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

		# Display the weather information in the terminal for debugging
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

		# Send the weather data and forecast to the HTML template
		return render_template(
			"index.html",
			weather = weather,
			forecast = forecast
		)

	return render_template("index.html", weather=None, forecast=None, error=None)

# Start the Flask development server when this file is run directly
if __name__ == "__main__":
	app.run()
