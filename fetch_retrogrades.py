import requests
import json
from datetime import datetime, timedelta
from skyfield.api import load, Topos

# Load planetary data
planets = load('de421.bsp')

# Define planets with their correct names from the kernel
planet_names = {
    'mercury': 'mercury',
    'venus': 'venus',
    'mars': 'mars',
    'jupiter': 'jupiter barycenter',
    'saturn': 'saturn barycenter',
    'uranus': 'uranus barycenter',
    'neptune': 'neptune barycenter'
}
planetary_objects = {name: planets[planet_names[name]] for name in planet_names}

# Define observer location (e.g., at the center of the Earth)
earth = planets['earth']
observer = earth + Topos(latitude_degrees=0, longitude_degrees=0)

# Function to calculate aspects
def calculate_aspects(date):
    ts = load.timescale()
    t = ts.utc(date.year, date.month, date.day)
    positions = {name: observer.at(t).observe(planet).apparent().ecliptic_latlon()[1].degrees for name, planet in planetary_objects.items()}
    
    aspects = []
    aspect_angles = {
        "conjunction": 0,
        "opposition": 180,
        "trine": 120,
        "square": 90,
        "sextile": 60,
        "quincunx": 150,
        "quintile": 72,
        "semi-sextile": 30,
        "semi-square": 45,
        "sesquiquadrate": 135
    }
    aspect_tolerance = 8  # Degrees of tolerance for aspects
    
    for planet1, lon1 in positions.items():
        for planet2, lon2 in positions.items():
            if planet1 != planet2:
                angle = abs(lon1 - lon2)
                for aspect, aspect_angle in aspect_angles.items():
                    if abs(angle - aspect_angle) <= aspect_tolerance or abs((angle + 360) - aspect_angle) <= aspect_tolerance:
                        aspects.append({
                            "planet1": planet1,
                            "planet2": planet2,
                            "aspect": aspect,
                            "angle": angle
                        })
    return aspects

# Function to fetch retrogrades
def fetch_retrogrades(start_date, days=7):
    base_url = "https://script.google.com/macros/s/AKfycbyEFPVkHdFU4jmP4yhY3hh5jrRG6uK155177KQrvZ1iQK5oLXa6UPc18G8gE4uq80H9TA/exec?date="
    retrogrades = []

    for i in range(days):
        date = start_date + timedelta(days=i)
        formatted_date = date.strftime('%Y-%m-%d')
        response = requests.get(base_url + formatted_date)

        if response.status_code == 200:
            data = response.json()
            if 'retrogrades' in data:
                retrogrades.extend(data['retrogrades'])
        else:
            print(f"Failed to fetch data for {formatted_date}: {response.status_code}")

    return retrogrades

# Function to generate notifications and educational content
def generate_notifications_and_education(weekly_forecast):
    notifications = []
    educational_content = []

    retrograde_alerts = []
    for day in weekly_forecast:
        for retrograde in day['retrogrades']:
            retrograde_alerts.append(f"{retrograde['body']} retrograde on {retrograde['date']}")

    if retrograde_alerts:
        notifications.append({
            "upcoming_retrograde_alert": ", ".join(retrograde_alerts),
            "daily_tip": "Reflect on the influences of the retrogrades."
        })
    else:
        notifications.append({
            "upcoming_retrograde_alert": "No upcoming retrogrades this week",
            "daily_tip": "Today is a good day to focus on your goals."
        })

    educational_content.append({
        "title": "Understanding Retrogrades",
        "url": "https://example.com/understanding-retrogrades"
    })
    educational_content.append({
        "title": "How to Navigate Retrogrades",
        "url": "https://example.com/navigate-retrogrades"
    })

    return notifications, educational_content

# Function to fetch aspects and retrogrades for the current week
def fetch_weekly_forecast(start_date, days=7):
    weekly_forecast = []
    retrogrades = fetch_retrogrades(start_date, days)

    for i in range(days):
        date = start_date + timedelta(days=i)
        aspects = calculate_aspects(date)
        daily_retrogrades = [r for r in retrogrades if r['date'] == date.strftime('%Y-%m-%d')]
        weekly_forecast.append({
            "date": date.strftime('%Y-%m-%d'),
            "retrogrades": daily_retrogrades,
            "aspects": aspects,
            "recommendations": {
                "do": ["Reflect on past decisions", "Backup important data", "Communicate clearly"],
                "dont": ["Start new projects", "Sign important contracts", "Make major purchases"]
            }
        })
    
    notifications, educational_content = generate_notifications_and_education(weekly_forecast)
    
    return {
        "weekly_forecast": weekly_forecast,
        "notifications": notifications,
        "educational_content": educational_content
    }

# Fetch data starting from today
start_date = datetime.now()
weekly_forecast_data = fetch_weekly_forecast(start_date)

# Save the data to a JSON file
def save_to_json(data, filename="weekly_forecast.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

save_to_json(weekly_forecast_data)

# Print the fetched data for verification
print(json.dumps(weekly_forecast_data, indent=4))
