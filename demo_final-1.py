import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
from geopy.geocoders import Nominatim

# Replace with your actual OpenWeatherMap API key
API_KEY = '6847e933e0d45b94da4c48d3afd9a43a'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
FORECAST_URL = 'http://api.openweathermap.org/data/2.5/forecast?'

# Global variable to store current latitude and longitude
current_lat = None
current_lon = None


def get_weather(city):
    """Fetches weather data from OpenWeatherMap API."""
    url = BASE_URL + 'appid=' + API_KEY + '&q=' + city + '&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror('Error', 'City not found or API error.')
        return None


def get_weather_by_coords(lat, lon):
    """Fetches weather data based on coordinates."""
    url = f'{BASE_URL}lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror('Error', 'Failed to retrieve weather for current location.')
        return None


def get_forecast_by_coords(lat, lon):
    """Fetches weather forecast data based on coordinates."""
    url = f'{FORECAST_URL}lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror('Error', 'Failed to retrieve weather forecast for current location.')
        return None


def display_weather():
    """Displays weather data in the GUI."""
    city_name = city_entry.get()
    if not city_name:
        messagebox.showerror('Error', 'Please enter a city name.')
        return

    weather_data = get_weather(city_name)

    if weather_data:
        update_weather_labels(weather_data)


def display_weather_by_coords(lat, lon):
    """Displays weather using latitude and longitude."""
    weather_data = get_weather_by_coords(lat, lon)
    if weather_data:
        update_weather_labels(weather_data)


def update_weather_labels(weather_data):
    """Updates the weather labels with the weather data."""
    try:
        temp = weather_data['main']['temp']
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        wind = weather_data['wind']['speed']
        cloudiness = weather_data['clouds']['all']
        description = weather_data['weather'][0]['description']
        timestamp = datetime.fromtimestamp(weather_data['dt']).strftime('%Y-%m-%d %H:%M:%S')

        # Update the labels with weather info
        temp_label.config(text=f'{temp} °C')
        pressure_label.config(text=f'{pressure} hPa')
        humidity_label.config(text=f'{humidity} %')
        wind_label.config(text=f'{wind} km/h')
        cloudiness_label.config(text=f'{cloudiness} %')
        description_label.config(text=description)
        timestamp_label.config(text=timestamp)

    except KeyError:
        messagebox.showerror('Error', 'Weather data incomplete.')
        reset_fields()


def display_forecast():
    """Displays weather forecast data in a new window for current location."""
    if current_lat is None or current_lon is None:
        messagebox.showerror('Error', 'Current location not set. Please use the current location first.')
        return

    forecast_data = get_forecast_by_coords(current_lat, current_lon)

    if forecast_data:
        forecast_window = tk.Toplevel(root)
        forecast_window.title('Weather Forecast')

        forecast_text = tk.Text(forecast_window, height=10, width=50)
        forecast_text.pack()

        for forecast in forecast_data['list']:
            timestamp = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d %H:%M:%S')
            temp = forecast['main']['temp']
            description = forecast['weather'][0]['description']
            forecast_text.insert(tk.END, f'{timestamp}: {temp} °C, {description}\n')


def use_current_location():
    """Fetches weather based on user's current location."""
    global current_lat, current_lon

    try:
        # Get public IP location
        ip_info = requests.get('http://ipinfo.io').json()
        loc = ip_info['loc'].split(',')
        current_lat, current_lon = float(loc[0]), float(loc[1])
        print(f"Latitude: {current_lat}, Longitude: {current_lon}")  # Debugging line

        # Display weather for the current coordinates
        display_weather_by_coords(current_lat, current_lon)

    except Exception as e:
        messagebox.showerror('Error', f'Failed to get current location: {e}')



def reset_fields():
    """Resets all input and output fields."""
    city_entry.delete(0, tk.END)
    temp_label.config(text='')
    pressure_label.config(text='')
    humidity_label.config(text='')
    wind_label.config(text='')
    cloudiness_label.config(text='')
    description_label.config(text='')
    timestamp_label.config(text='')


# --- GUI Setup ---
root = tk.Tk()
root.title('Weather Application')
root.geometry('500x400')
root.configure(bg='lightblue')

# City input
city_label = tk.Label(root, text='Enter City:', bg='lightblue')
city_label.grid(row=0, column=0, padx=10, pady=10)
city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)

# Buttons
get_weather_button = tk.Button(root, text='Get Weather', command=display_weather, bg='green', fg='white')
get_weather_button.grid(row=0, column=2, padx=10, pady=10)

current_location_button = tk.Button(root, text='Use Current Location', command=use_current_location, bg='orange',
                                    fg='white')
current_location_button.grid(row=1, column=1, pady=10)

get_forecast_button = tk.Button(root, text='Weather Forecast', command=display_forecast, bg='blue', fg='white')
get_forecast_button.grid(row=1, column=2, pady=10)

# Weather details labels
tk.Label(root, text='Temperature:', bg='lightblue').grid(row=2, column=0, padx=10, pady=5)
temp_label = tk.Label(root, text='', bg='lightblue')
temp_label.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text='Pressure:', bg='lightblue').grid(row=3, column=0, padx=10, pady=5)
pressure_label = tk.Label(root, text='', bg='lightblue')
pressure_label.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text='Humidity:', bg='lightblue').grid(row=4, column=0, padx=10, pady=5)
humidity_label = tk.Label(root, text='', bg='lightblue')
humidity_label.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text='Wind Speed:', bg='lightblue').grid(row=5, column=0, padx=10, pady=5)
wind_label = tk.Label(root, text='', bg='lightblue')
wind_label.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text='Cloudiness:', bg='lightblue').grid(row=6, column=0, padx=10, pady=5)
cloudiness_label = tk.Label(root, text='', bg='lightblue')
cloudiness_label.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text='Description:', bg='lightblue').grid(row=7, column=0, padx=10, pady=5)
description_label = tk.Label(root, text='', bg='lightblue')
description_label.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text='Timestamp:', bg='lightblue').grid(row=8, column=0, padx=10, pady=5)
timestamp_label = tk.Label(root, text='', bg='lightblue')
timestamp_label.grid(row=8, column=1, padx=10, pady=5)

# Reset button
reset_button = tk.Button(root, text='Reset', command=reset_fields, bg='gray', fg='white')
reset_button.grid(row=9, column=1, pady=10)

root.mainloop()
