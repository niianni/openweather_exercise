from glob import glob
import os
import pandas as pd

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
data_dir = CURR_DIR_PATH + "/data/"
target_dir = CURR_DIR_PATH + "/target/"

# This function extracts data from multiple files
def load_dfs_from(glob_path):
    subject_data = []
    file_paths = glob(glob_path) # Gets a list of glob matches, ex. all csv files in target/late

    for path in file_paths:
        df = pd.read_csv(path)
        subject_data.append(df) # Appends a dataframe of stored data to the returned data
    
    return subject_data, file_paths # Returns a list of dataframes, and extracted files paths

# Transform the data
def transform_weather():
    data, paths = load_dfs_from(f"{data_dir}*.csv")
    weather_data = []

    for path, entry in zip(paths, data):
        entry = entry.to_dict("records")[0]
        weather_entry = {
            "city": os.path.basename(path)[:-4], # Remove ".csv" at the end
            "tempature": entry["main.temp"] - 273, # Convert to Celsius from Kelvin
            "weather": entry["weather.main"],
            "weather_desc": entry["weather.description"],
            "cloudy": entry["clouds.all"],
            "humid": entry["main.humidity"]
        }
        weather_data.append(weather_entry)

    df = pd.DataFrame(weather_data, columns=["city", "tempature", "weather", "weather_desc", "cloudy", "humid"])
    df.to_csv(target_dir + "final_weather.csv", index=False)


