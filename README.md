# 🌤️ Weather Dashboard

A simple and responsive weather dashboard built with **Python and Flask**. Search for a city to view the current weather and a 5-day forecast.

The application can be run locally with Python or inside a **Docker container**.

## ✨ Features

* 🔎 Search weather by city
* 🌡️ Current temperature
* 💧 Humidity
* 💨 Wind speed
* 🌤️ Current weather conditions
* 📅 5-day weather forecast
* 🌦️ Weather icons and readable weather descriptions
* ❌ Error handling for invalid cities and API connection issues
* 🐳 Docker support

## 🛠️ Tech Stack

* **Python**
* **Flask**
* **HTML / CSS**
* **JavaScript**
* **Open-Meteo API**
* **Requests**
* **Docker**

## ⚙️ How It Works

1. Enter a city name in the search field.
2. The application uses the **Open-Meteo Geocoding API** to find the city's coordinates.
3. The coordinates are used to request current weather and forecast data.
4. The weather information is processed by the Flask backend.
5. The data is displayed in the dashboard.

## 🚀 Getting Started

### Prerequisites

Choose one of the following:

**Option 1 — Docker**

* Docker Desktop

**Option 2 — Local Python**

* Python 3.x
* pip

---

## 🐳 Run with Docker

Docker is the easiest way to run the application without manually installing the Python dependencies.

### 1. Clone the repository

```bash
git clone https://github.com/weyn-n/weather-dashboard.git
cd weather-dashboard
```

### 2. Build the Docker image

```bash
docker build -t weather-dashboard .
```

### 3. Run the container

```bash
docker run -p 5000:5000 weather-dashboard
```

The application will be available at:

```text
http://localhost:5000
```

### Stop the container

Press `Ctrl + C` in the terminal where the container is running.

Alternatively, if running in detached mode:

```bash
docker ps
docker stop <container_id>
```

### Rebuild after changes

If you change the application code, rebuild the image:

```bash
docker build -t weather-dashboard .
```

Then run the container again:

```bash
docker run -p 5000:5000 weather-dashboard
```

---

## 🐍 Run Locally Without Docker

### 1. Clone the repository

```bash
git clone https://github.com/weyn-n/weather-dashboard.git
cd weather-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Then open:

```text
http://localhost:5000
```

## 📁 Project Structure

```text
weather-dashboard/
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🌐 API

Weather data is provided by **Open-Meteo**.

The application uses:

* **Geocoding API** — converts a city name into geographic coordinates.
* **Weather API** — provides current weather and forecast data.

## 🐳 Docker

The project includes a `Dockerfile` that packages the Flask application together with its Python dependencies.

This makes the application:

* portable across different environments
* easier to set up
* independent of the host Python environment
* reproducible

## 🌍 Live Demo

The application is also deployed online:

https://weather-dashboard-pfyk.onrender.com/