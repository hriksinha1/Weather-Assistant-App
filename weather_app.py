import os
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={os.getenv('WEATHER_API_KEY')}&q={location}"

    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['main']
        # Convert Kelvin to Celsius or Fahrenheit
        if unit == "fahrenheit":
            temperature = (data['main']['temp'] - 273.15) * 9/5 + 32
        else:
            temperature = data['main']['temp'] - 273.15
        return {
            "city": location,
            "weather": weather,
            "temperature": round(temperature, 2)
        }
    else:
        return {"city": location, "weather": "Data Fetch Error", "temperature": "N/A"}

def main():
    st.title("Weather Information App")

    location = st.text_input("Enter a location (e.g., London):")
    if st.button("Get Weather"):
        if location:
            weather_data = get_current_weather(location)
            if weather_data["weather"] != "Data Fetch Error":
                st.subheader(f"Weather in {weather_data['city']}:")
                st.write(f"Weather: {weather_data['weather']}")
                st.write(f"Temperature: {weather_data['temperature']}°F")
            else:
                st.error("Failed to fetch weather data. Please try again.")
        else:
            st.error("Please enter a location.")
    elif not location:
        st.error("Please enter a location.") 

if __name__ == "__main__":
    main()