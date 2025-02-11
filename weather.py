import requests

def get_weather(location):
    url = f"http://wttr.in/{location}?format=j1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        response.close()  # Close the connection
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

weather_icons = {
    "sunny": "☀️",
    "clear": "☀️",
    "cloudy": "☁️",
    "overcast": "☁️",
    "rain": "🌧️",
    "thunderstorm": "⛈️",
    "storm": "⛈️"
}

def draw_weather(weather_condition):
    for condition, icon in weather_icons.items():
        if condition in weather_condition.lower():
            print(icon)
            return
    print("Unknown weather condition")

def main():
    while True:
        location = input("Enter your location (city or zip code): ")
        print("\n====================\n")
        weather_data = get_weather(location)
        if weather_data is None:
            print("Failed to retrieve weather data.")
            continue

        print("Current Weather:")
        try:
            print("----------")
            print(f"Temperature: {weather_data['current_condition'][0]['temp_C']}°C ({weather_data['current_condition'][0]['temp_F']}°F)")
            print(f"Weather Condition: {weather_data['current_condition'][0]['weatherDesc'][0]['value']}")
            draw_weather(weather_data['current_condition'][0]['weatherDesc'][0]['value'])
            print(f"Humidity: {weather_data['current_condition'][0]['humidity']}%")
            print(f"Wind Speed: {weather_data['current_condition'][0]['winddir16Point']} {weather_data['current_condition'][0]['windspeedKmph']} km/h ({weather_data['current_condition'][0]['windspeedMiles']} mph)")
            print(f"Atmospheric Pressure: {weather_data['current_condition'][0]['pressure']} hPa ({weather_data['current_condition'][0]['pressure']} mbar)")
        except KeyError as e:
            print(f"Error: Missing key {e}")

        print("\n====================\n")

        print("Forecast:")
        try:
            for day in weather_data['weather']:
                print("----------")
                print(f"Date: {day['date']}")
                print(f"Temperature: High = {day['maxtempC']}°C ({day['maxtempF']}°F) | Low = {day['mintempC']}°C ({day['mintempF']}°F)")
                print(f"Weather Condition: {day['hourly'][0]['weatherDesc'][0]['value']}")
                draw_weather(day['hourly'][0]['weatherDesc'][0]['value'])
                print(f"Chance of Precipitation: {day['hourly'][0]['precipMM']} mm")
        except KeyError as e:
            print(f"Error: Missing key {e}")

        print("\n====================\n")

        if 'moon_phase' in weather_data:
            print("Moon Phase:")
            try:
                print(f"Moon Age: {weather_data['moon_phase']['ageOfMoon']} days")
                print(f"Moon Phase: {weather_data['moon_phase']['phaseofMoon']}")
            except KeyError as e:
                print(f"Error: Missing key {e}")
        else:
            print("Moon Phase: Not available")
        
        print("\n====================\n")

        if 'astronomy' in weather_data:
            print("Sunrise and Sunset Times:")
            try:
                print(f"Sunrise: {weather_data['astronomy'][0]['sunrise']}")
                print(f"Sunset: {weather_data['astronomy'][0]['sunset']}")
                print(f"Civil Twilight: {weather_data['astronomy'][0]['civil_twilight_begin']} - {weather_data['astronomy'][0]['civil_twilight_end']}")
                print(f"Nautical Twilight: {weather_data['astronomy'][0]['nautical_twilight_begin']} - {weather_data['astronomy'][0]['nautical_twilight_end']}")
                print(f"Astronomical Twilight: {weather_data['astronomy'][0]['astronomical_twilight_begin']} - {weather_data['astronomy'][0]['astronomical_twilight_end']}")
            except KeyError as e:
                print(f"Error: Missing key {e}")
        else:
            print("Sunrise and Sunset Times: Not available")

        print("\n====================\n")

        choice = input("Enter 1 to check another location, 2 to exit: ")
        if choice == "1":
            continue
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()