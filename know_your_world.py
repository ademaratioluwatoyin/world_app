import streamlit as st
import requests

st.set_page_config(page_title="Know the World", page_icon="🌍")
st.title("🌍 Know the World")

# Input: Country name
country_name = st.text_input("Enter a country name (e.g., Nigeria, Japan, Brazil):")

if country_name:
    # Get country data
    with st.spinner("Fetching country info..."):
        country_response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")

    if country_response.status_code != 200:
        st.error("❌ Could not find country. Please check the spelling.")
    else:
        data = country_response.json()[0]
        capital = data.get("capital", ["N/A"])[0]
        population = data.get("population", "N/A")
        region = data.get("region", "N/A")
        flag_url = data.get("flags", {}).get("png", "")
        latlng = data.get("capitalInfo", {}).get("latlng", [None, None])

        # Display country info
        st.subheader(f"📍 {country_name.capitalize()} Info")
        st.markdown(f"**🏛 Capital:** {capital}")
        st.markdown(f"**🌍 Region:** {region}")
        st.markdown(f"**👥 Population:** {population:,}")
        if flag_url:
            st.image(flag_url, width=150, caption="National Flag")

        # Get weather if coordinates are available
        if None not in latlng:
            lat, lon = latlng
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current_weather=true"
            )
            weather_response = requests.get(weather_url)
            if weather_response.status_code == 200:
                weather = weather_response.json()["current_weather"]
                st.subheader(f"🌡️ Weather in {capital}")
                st.markdown(f"**Temperature:** {weather['temperature']} °C")
                st.markdown(f"**Wind Speed:** {weather['windspeed']} km/h")
            else:
                st.warning("⚠️ Weather data not available.")
        else:
            st.warning("⚠️ No capital location data available.")
