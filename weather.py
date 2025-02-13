import requests
import sys
import os
import re

# Force UTF-8 encoding for stdout
sys.stdout.reconfigure(encoding='utf-8')

# Enable ANSI escape sequence processing on Windows
if os.name == 'nt':
    os.system('color')

# Regular expression to match ANSI escape codes
def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mK]')
    return ansi_escape.sub('', text)

def get_ip_address():
    """Gets the IP address of the machine."""
    try:
        response = requests.get('https://api.ipify.org')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_location(ip_address):
    """Gets the location associated with the IP address."""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip_address}')
        response.raise_for_status()
        data = response.json()
        return f"{data['city']}, {data['country']}"
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_weather(location):
    try:
        url = f"http://wttr.in/{location}?format=j1"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    except ValueError as e:
        print(f"Error: Invalid location - {e}")
        return None

weather_icons = {
    "unknown": [
        "\033[0m .——.  \033[0m",
        "\033[0m     ) \033[0m",
        "\033[0m    /  \033[0m",
        "\033[0m   '   \033[0m",
        "\033[0m   •   \033[0m",
    ],
    "sunny": [
        "\033[38;5;226m    \\ . /    \033[0m",
        "\033[38;5;226m   - .-. -   \033[0m",
        "\033[38;5;226m  ‒ (   ) ‒  \033[0m",
        "\033[38;5;226m   . `-᾿ .   \033[0m",
        "\033[38;5;226m    / ' \\    \033[0m",
    ],
    "partly cloudy": [
        "\033[38;5;226m   \\__/\033[0m      ",
        "\033[38;5;226m __/  \033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m   \\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "             ",
    ],
    "cloudy": [
        "\033[0m", # ANSI escape code: reset to default color
        "\033[38;5;250m     .--.    \033[0m",
        "\033[38;5;250m  .-(    ).  \033[0m",
        "\033[38;5;250m (___.__)__) \033[0m",
        "\033[0m", # ANSI escape code: reset to default color
    ],
    "very cloudy": [
        "\033[0m", # ANSI escape code: reset to default color
        "\033[38;5;244;1m     .--.    \033[0m",
        "\033[38;5;244;1m  .-(    ).  \033[0m",
        "\033[38;5;244;1m (___.__)__) \033[0m",
        "\033[0m", # ANSI escape code: reset to default color
    ],
    "fog": [
        "\033[0m", # ANSI escape code: reset to default color
        "\033[38;5;251m _ - _ - _ - \033[0m",
        "\033[38;5;251m  _ - _ - _  \033[0m",
        "\033[38;5;251m _ - _ - _ - \033[0m",
        "\033[0m", # ANSI escape code: reset to default color
    ],
    "light rain": [
        "\033[38;5;250m     .-.     \033[0m",
        "\033[38;5;250m    (   ).   \033[0m",
        "\033[38;5;250m   (___(__)  \033[0m",
        "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
        "\033[38;5;111m   ʻ ʻ ʻ ʻ   \033[0m",
    ],
    "heavy rain": [
        "\033[38;5;244;1m     .-.     \033[0m",
        "\033[38;5;244;1m    (   ).   \033[0m",
        "\033[38;5;244;1m   (___(__)  \033[0m",
        "\033[38;5;33;1m  ‚ʻ‚ʻ‚ʻ‚ʻ   \033[0m",
        "\033[38;5;33;1m  ‚ʻ‚ʻ‚ʻ‚ʻ   \033[0m",
    ],
    "light showers": [
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;111m     ʻ ʻ ʻ ʻ \033[0m",
        "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
    ],
    "heavy showers": [
        "\033[38;5;226m _`/\"\"\033[38;5;244;1m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;244;1m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;244;1m(___(__) \033[0m",
        "\033[38;5;33;1m   ‚ʻ‚ʻ‚ʻ‚ʻ  \033[0m",
        "\033[38;5;33;1m   ‚ʻ‚ʻ‚ʻ‚ʻ  \033[0m",
    ],
    "light snow": [
        "\033[38;5;250m     .-.     \033[0m",
        "\033[38;5;250m    (   ).   \033[0m",
        "\033[38;5;250m   (___(__)  \033[0m",
        "\033[38;5;255m    *  *  *  \033[0m",
        "\033[38;5;255m   *  *  *   \033[0m",
    ],
    "heavy snow": [
        "\033[38;5;244;1m     .-.     \033[0m",
        "\033[38;5;244;1m    (   ).   \033[0m",
        "\033[38;5;244;1m   (___(__)  \033[0m",
        "\033[38;5;255;1m   * * * *   \033[0m",
        "\033[38;5;255;1m  * * * *    \033[0m",
    ],
    "light snow showers": [
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;255m     *  *  * \033[0m",
        "\033[38;5;255m    *  *  *  \033[0m",
    ],
    "heavy snow showers": [
        "\033[38;5;226m _`/\"\"\033[38;5;244;1m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;244;1m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;244;1m(___(__) \033[0m",
        "\033[38;5;255;1m    * * * *  \033[0m",
        "\033[38;5;255;1m   * * * *   \033[0m",
    ],
    "light sleet": [
        "\033[38;5;250m     .-.     \033[0m",
        "\033[38;5;250m    (   ).   \033[0m",
        "\033[38;5;250m   (___(__)  \033[0m",
        "\033[38;5;111m    ʻ \033[38;5;255m*\033[38;5;111m ʻ \033[38;5;255m*  \033[0m",
        "\033[38;5;255m   *\033[38;5;111m ʻ \033[38;5;255m*\033[38;5;111m ʻ   \033[0m",
    ],
    "light sleet showers": [
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;111m     ʻ \033[38;5;255m*\033[38;5;111m ʻ \033[38;5;255m* \033[0m",
        "\033[38;5;255m    *\033[38;5;111m ʻ \033[38;5;255m*\033[38;5;111m ʻ  \033[0m",
    ],
    "thundery showers": [
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;228;5m    ⚡\033[38;5;111;25mʻ ʻ\033[38;5;228;5m⚡\033[38;5;111;25mʻ ʻ \033[0m",
        "\033[38;5;111m    ʻ ʻ ʻ ʻ  \033[0m",
    ],
    "thundery heavy rain": [
        "\033[38;5;244;1m     .-.     \033[0m",
        "\033[38;5;244;1m    (   ).   \033[0m",
        "\033[38;5;244;1m   (___(__)  \033[0m",
        "\033[38;5;33;1m  ‚ʻ\033[38;5;228;5m⚡\033[38;5;33;25mʻ‚\033[38;5;228;5m⚡\033[38;5;33;25m‚ʻ   \033[0m",
        "\033[38;5;33;1m  ‚ʻ‚ʻ\033[38;5;228;5m⚡\033[38;5;33;25mʻ‚ʻ   \033[0m",
    ],
    "thundery snow showers": [
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;255m     *\033[38;5;228;5m⚡\033[38;5;255;25m *\033[38;5;228;5m⚡\033[38;5;255;25m * \033[0m",
        "\033[38;5;255m    *  *  *  \033[0m",
    ],
}

def color_temp(temp):
    colmap = [
        (-15, 21), (-12, 27), (-9, 33), (-6, 39), (-3, 45),
        (0, 51), (2, 50), (4, 49), (6, 48), (8, 47),
        (10, 46), (13, 82), (16, 118), (19, 154), (22, 190),
        (25, 226), (28, 220), (31, 214), (34, 208), (37, 202),
    ]
    col = 196
    for max_temp, color in colmap:
        if temp < max_temp:
            col = color
            break
    return f"\033[38;5;{col}m{int(temp)}\033[0m"

def draw_weather(weather_condition):
    for condition, icon in weather_icons.items():
        if condition in weather_condition.lower():
            print(icon)
            return
    print("Unknown weather condition")

def wind_direction(deg):
    """Convert wind direction in degrees to a compass direction."""
    if deg is None:
        return "?"
    
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = round(deg / 22.5) % 16
    return directions[index]

def display_weather_data(weather_data):
    print(f"Weather for {weather_data['nearest_area'][0]['areaName'][0]['value']}")
    
    current = weather_data['current_condition'][0]
    condition = current['weatherDesc'][0]['value'].lower()
    icon = weather_icons.get(condition, weather_icons['sunny'])
    
    print("\nCurrent weather:")
    for line in icon:
        print(f"{line:<50}")
    print('─'*32)
    print(f"Temperature: {color_temp(float(current['temp_C']))}°C ({color_temp(float(current['temp_F']))}°F)")
    print(f"Wind: {wind_direction(int(current['winddirDegree']))} {color_temp(float(current['windspeedKmph']))} km/h")
    print(f"Humidity: {current['humidity']}%")
    print(f"Visibility: {current['visibility']} km")

    print("\nForecast:")
    for day in weather_data['weather']:
        print(f"\n{day['date']}:")
        print("┌────────┬────────────────┬────────────┬────────────┐")
        print("│  Time  │      Temp      │    Wind    │    Rain    │")
        print("├────────┼────────────────┼────────────┼────────────┤")
        for hour in day['hourly']:
            time = f"{int(hour['time'])//100:02d}:00"
            temp_c = float(hour['tempC'])
            temp_f = (temp_c * 9/5) + 32  # Convert Celsius to Fahrenheit
            temp = f"{color_temp(temp_c)}°C/{color_temp(temp_f)}°F"
            wind = f"{wind_direction(int(hour['winddirDegree']))} {hour['windspeedKmph']}"
            rain = f"{hour['precipMM']} mm"
            print(f"│ {time:<6} │ {temp:<42} │ {wind:<10} │ {rain:<10} │") # TODO: Adjust dynamic column width for colored temp
        print("└────────┴────────────────┴────────────┴────────────┘")
        # print("len(plain_temp) =", len(strip_ansi_codes(temp)), "len(temp) =", len(temp)) # Debugging

def main():
    ip_address = get_ip_address()
    if ip_address is None:
        print("Failed to get IP address.")
        return

    location = get_location(ip_address)
    if location is None:
        print("Failed to get location.")
        return

    user_defined_location = None

    while True:
        if user_defined_location is None:
            weather_data = get_weather(location)
            print(f"Current Weather for {location} ({ip_address}):")
        else:
            weather_data = get_weather(user_defined_location)
            print(f"Current Weather for {user_defined_location}:")
        
        if weather_data is None:
            print("Failed to get weather data.")
            return

        display_weather_data(weather_data)

        choice = input("\nEnter 1 to check another location, 2 to exit: ")
        if choice == "1":
            while True:
                print(f"\n{'─' * 46}\n") # Query separator
                user_defined_location = input("Enter your location (city or zip code): ")
                try:
                    weather_data = get_weather(user_defined_location)
                    if weather_data is not None:
                        break
                    else:
                        print("Invalid location. Please try again.")
                except Exception as e:
                    print(f"Error: {e}")
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()