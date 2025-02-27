import requests, os, configparser
import pandas as pd

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# Initializes configuration from the config.ini file
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/config.ini")

# Fetches the api key from your config.ini file
API_KEY = config.get("DEV", "API_KEY")

# URL without parameters (lon=...&lat=...&appid=...)
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# Pre-defined geo-coordinates for some cities, feel free to add/remove more using google maps
# Don't go too crazy though, as the script will perform one API call per city!
geo_locations = {
    "tampere": (61.498100, 23.760890),
    "pori": (61.486599, 21.796788),
    "helsinki": (60.167640, 24.954443),
    "turku": (60.451515, 22.267119)
}

def request_new_weather_data():
    # For every city, fetch and store weather data
    for city in geo_locations:
        (lat, lon) = geo_locations[city]

        # The parameters for the REST API call
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }

        # Fetching the data using HTTP method GET
        # URL using the params parameter will become:
        #   https://api.openweathermap.org/data/2.5/weather?lat=...&lon=...&appid=<your_key>
        r = requests.get(WEATHER_URL, params=params)
        
        print("url:", r.url) # Should ressemble link from above, else check params dictionary
        print("http code:", r.status_code) # Should be 200, else check key

        if r.status_code == 200: # If connection is successful (200: http ok)
            json_data = r.json() # Get result in json

            # Create a dictionary to represent the stored data
            # To view all accessible data see: https://openweathermap.org/current#current_JSON
            weather_data = {
                "weather": json_data["weather"][0], # [0] because for some reason it's a single element list?
                "main": json_data["main"],
                "visibility": json_data["visibility"],
                "wind": json_data["wind"],
                "clouds": json_data["clouds"]
            }
            # Flattens dictionaries (normalize) because a dataframe can't contain nested dictionaries
            # E.g. Internal dictionary {"weather": {"temp": 275, "max_temp": 289}}
            # becomes {"weather.temp": 275, "weather.max_temp", 289}
            weather_data = pd.json_normalize(weather_data) 

            df = pd.DataFrame(weather_data)
            df.to_csv(CURR_DIR_PATH + "/data/" + city + ".csv", index=False)
            

            


