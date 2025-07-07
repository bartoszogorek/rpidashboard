from flask import Flask, render_template
import psutil
import os
import time

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
