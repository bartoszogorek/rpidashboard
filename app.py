from flask import Flask, render_template
import psutil
import os
import time
import requests

app = Flask(__name__)

API_KEY = "TU_WKLEJ_SWÓJ_KLUCZ_API"  # <- Zmień na swój klucz OpenWeather

def get_temp():
    try:
        temp = os.popen("vcgencmd measure_temp").readline()
        return temp.replace("temp=", "").strip()
    except:
        return "N/A"

def get_uptime():
    uptime_seconds = time.time() - psutil.boot_time()
    hours, remainder = divmod(int(uptime_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m"

def get_weather(city="Krakow"):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={a083184d75364d652b377de5c77ac508}&units=metric&lang=pl"
        response = requests.get(url)
        data = response.json()
        weather = {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize(),
            "humidity": data["main"]["humidity"]
        }
        return weather
    except:
        return None

@app.route("/")
def index():
    cpu_temp = get_temp()
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    uptime = get_uptime()
    return render_template("dashboard.html",
                           cpu_temp=cpu_temp,
                           cpu_usage=cpu_usage,
                           memory_percent=memory.percent,
                           uptime=uptime)

@app.route("/pogoda")
def pogoda():
    weather = get_weather("Krakow")
    return render_template("pogoda.html", weather=weather)

@app.route("/mapa")
def mapa():
    return render_template("mapa.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
