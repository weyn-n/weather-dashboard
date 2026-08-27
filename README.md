# Weather Dashboard

A simple weather dashboard built with **Python** and **Flask**.
Search for a city to view the current weather and a 5-day forecast.

## Features

* Search weather by city
* Current temperature, humidity, wind speed, and weather conditions
* 5-day weather forecast
* Weather icons and readable weather descriptions
* Error handling for invalid cities and API connection issues

## Tech Stack

* Python
* Flask
* HTML / CSS
* Open-Meteo API
* Requests

## How It Works

1. Enter a city name in the search field.
2. The app uses the **Open-Meteo Geocoding API** to find the city's coordinates.
3. The coordinates are used to request current weather and forecast data.
4. The weather information is displayed in the dashboard.

## Installation

Clone the repository:

```bash
git clone https://github.com/weyn-n/weather-dashboard.git
cd weather-dashboard
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Start the Flask development server:

```bash
python app.py
```

Then open the local address shown in your terminal.

## Project Structure

```text
weather-dashboard/
├── static/
├──── script.js
├──── style.css
├── templates/
├──── index.html
├── app.py
├── README.md
└── requirements.tx
```

## API

Weather data is provided by [Open-Meteo](https://open-meteo.com/).