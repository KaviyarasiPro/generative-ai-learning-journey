''' Day 9 - Weather Data Fetcher
Fetch real-time weather information using the Open-Meteo API'''


# Import requests library to communicate with the API
import requests

city = input("Enter city name: ")


# Create the Geocoding API URL
# This API converts the city name into latitude and longitude
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"


# Send a GET request to the Geocoding API
response = requests.get(geo_url)


# Convert the JSON response into Python data
data = response.json()


# Extract latitude and longitude from the first search result
latitude = data["results"][0]["latitude"]
longitude = data["results"][0]["longitude"]


# Create the Weather API URL using latitude and longitude
# Request current temperature, humidity, weather code and wind speed
weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"


# Send a GET request to the Weather API
weather_response = requests.get(weather_url)


# Convert the weather API JSON response into Python data
weather_data = weather_response.json()


# Extract the current weather section
current = weather_data["current"]


# Extract individual weather values
temperature = current["temperature_2m"]
humidity = current["relative_humidity_2m"]
weather_code = current["weather_code"]
wind_speed = current["wind_speed_10m"]


# Convert the numeric weather code into a readable condition
if weather_code == 0:
    condition = "Clear Sky"

elif weather_code in [1, 2, 3]:
    condition = "Cloudy"

elif weather_code in [45, 48]:
    condition = "Foggy"

elif weather_code in [51, 53, 55, 61, 63, 65]:
    condition = "Rainy"

elif weather_code in [71, 73, 75]:
    condition = "Snowy"

elif weather_code in [95, 96, 99]:
    condition = "Thunderstorm"

else:
    condition = "Unknown"


# Display the final weather report
print("\n================================")
print("         WEATHER REPORT")
print("================================")

print("City        :", city)
print("Temperature :", temperature, "°C")
print("Condition   :", condition)
print("Humidity    :", humidity, "%")
print("Wind Speed  :", wind_speed, "km/h")

print("================================")
