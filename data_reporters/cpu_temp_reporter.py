import subprocess
import requests


URL = "http://localhost:8000/data-logger/measurements/"
TOKEN = "adbea5f168f9bc36690608291d1c2f2eb7600e7d"
SENSOR = 1


def main():
    header = {
        "Authorization": f"Token {TOKEN}",
    }
    payload = {
        "sensor": SENSOR,
        "value": get_cpu_temp(),
    }
    requests.post(URL, header=header, json=payload)


def get_cpu_temp():
    command = r"vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'"
    temp_reading = subprocess.run(command, shell=True, check=True)
    return int(temp_reading)


if __name__ == "__main__":
    main()