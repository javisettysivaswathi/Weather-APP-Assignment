import os
import sqlite3
import requests
import csv
import json
from dotenv import load_dotenv

load_dotenv()

DB_NAME = "weather.db"
API_KEY = os.getenv("OWN_API_KEY")
BASE_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        date TEXT,
        temp REAL,
        description TEXT
    )
    ''')
    conn.commit()
    conn.close()

def get_current_weather(city):
    if not API_KEY:
        print("❌ ERROR: Please set your OpenWeatherMap API key in environment variable 'OWN_API_KEY'.")
        return None
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_WEATHER_URL, params=params)
    if resp.status_code != 200:
        return None
    data = resp.json()
    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "desc": data["weather"][0]["description"].capitalize()
    }

def get_5day_forecast(city):
    if not API_KEY:
        print("❌ ERROR: Please set your OpenWeatherMap API key in environment variable 'OWN_API_KEY'.")
        return None
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_FORECAST_URL, params=params)
    if resp.status_code != 200:
        return None
    data = resp.json()
    forecast = []
    # The API returns data every 3 hours, pick those at 12:00:00 each day
    for item in data['list']:
        if "12:00:00" in item['dt_txt']:
            forecast.append({
                "date": item['dt_txt'].split()[0],
                "temp": item['main']['temp'],
                "desc": item['weather'][0]['description'].capitalize()
            })
    return forecast

def create_weather_record(city):
    weather = get_current_weather(city)
    if not weather:
        return False
    date_str = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO weather (city, date, temp, description) VALUES (?, ?, ?, ?)",
              (weather['city'], date_str, weather['temp'], weather['desc']))
    conn.commit()
    conn.close()
    return True

def read_all_records():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM weather ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def update_record(record_id, temp, desc):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE weather SET temp=?, description=? WHERE id=?", (temp, desc, record_id))
    conn.commit()
    conn.close()

def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM weather WHERE id=?", (record_id,))
    conn.commit()
    conn.close()

def export_to_csv():
    rows = read_all_records()
    filename = "weather_export.csv"
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "City", "Date", "Temperature", "Description"])
        writer.writerows(rows)
    return filename

def export_to_json():
    rows = read_all_records()
    filename = "weather_export.json"
    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "city": r[1],
            "date": r[2],
            "temp": r[3],
            "description": r[4]
        })
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return filename

def generate_google_maps_link(city):
    return f"https://www.google.com/maps/search/{city.replace(' ', '+')}"

def get_youtube_search_link(city):
    return f"https://www.youtube.com/results?search_query={city.replace(' ', '+')}+travel"

