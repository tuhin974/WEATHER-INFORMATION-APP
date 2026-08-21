import streamlit as st
from datetime import datetime

from weather_api import fetch_weather
from data_processing import create_dataframe, clean_data
from visualization import (
    line_chart,
    bar_chart,
    heatmap,
    pie_chart
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Weather Information & Analytics",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CACHED WEATHER API FUNCTION
# ==================================================

@st.cache_data(ttl=300)
def get_weather(city):
    """
    Fetch and cache weather information for a city.

    Cached for 5 minutes to reduce unnecessary
    API requests during Streamlit reruns.
    """
    return fetch_weather(city)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🌦️ Weather App")

st.sidebar.write(
    "Real-time weather information and analytics"
)

st.sidebar.markdown("---")

st.sidebar.subheader("🛠️ Technologies")

st.sidebar.write("🐍 Python")
st.sidebar.write("🌐 OpenWeatherMap API")
st.sidebar.write("📦 REST API / JSON")
st.sidebar.write("📊 Pandas")
st.sidebar.write("📈 Matplotlib")
st.sidebar.write("🎨 Seaborn")
st.sidebar.write("🖥️ Streamlit")

st.sidebar.markdown("---")

st.sidebar.subheader("📌 Features")

st.sidebar.write("🔍 City Search")
st.sidebar.write("🌡️ Current Weather")
st.sidebar.write("📊 Multi-City Comparison")
st.sidebar.write("📈 Weather Analytics")
st.sidebar.write("🛡️ API Error Handling")
st.sidebar.write("⚡ API Response Caching")


# ==================================================
# MAIN HEADER
# ==================================================

st.title("🌦️ Weather Information & Analytics App")

st.write(
    "Fetch, analyze, and compare real-time weather "
    "information using the OpenWeatherMap API."
)

st.caption(
    f"Last Updated: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)


# ==================================================
# CITY SEARCH
# ==================================================

st.markdown("---")

st.header("🔍 Search for a City")

st.write(
    "Enter a city name to retrieve its current weather information."
)


# Search input and button
search_col, button_col = st.columns([4, 1])

with search_col:

    city = st.text_input(
        "City",
        placeholder="Enter a city name, e.g. Kolkata",
        label_visibility="collapsed"
    )

with button_col:

    search_clicked = st.button(
        "Get Weather",
        type="primary",
        use_container_width=True
    )


# ==================================================
# SEARCH WEATHER RESULT
# ==================================================

if search_clicked:

    # ----------------------------------------------
    # Validate city input
    # ----------------------------------------------

    if not city.strip():

        st.warning(
            "⚠️ Please enter a city name."
        )

    else:

        city_name = city.strip()

        # ------------------------------------------
        # Fetch weather
        # ------------------------------------------

        with st.spinner(
            f"Fetching weather data for {city_name}..."
        ):

            result = get_weather(city_name)


        # ------------------------------------------
        # Handle API error
        # ------------------------------------------

        if not result["success"]:

            st.error(
                f"❌ {result['error']}"
            )


        # ------------------------------------------
        # Display weather
        # ------------------------------------------

        else:

            weather = result["data"]

            st.success(
                f"✅ Weather information retrieved for "
                f"{weather['City']}, {weather['Country']}"
            )

            # --------------------------------------
            # Location and Weather Condition
            # --------------------------------------

            icon_url = (
                "https://openweathermap.org/img/wn/"
                f"{weather['Icon']}@2x.png"
            )

            icon_col, location_col = st.columns(
                [1, 5]
            )

            with icon_col:

                st.image(
                    icon_url,
                    width=100
                )

            with location_col:

                st.subheader(
                    f"{weather['City']}, "
                    f"{weather['Country']}"
                )

                st.write(
                    weather["Description"].title()
                )

                st.caption(
                    f"Weather data retrieved at "
                    f"{weather['Date']}"
                )


            # --------------------------------------
            # Main Weather Metrics
            # --------------------------------------

            st.markdown("### 🌡️ Current Conditions")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Temperature",
                f"{weather['Temperature']:.1f} °C"
            )

            col2.metric(
                "Feels Like",
                f"{weather['Feels Like']:.1f} °C"
            )

            col3.metric(
                "Humidity",
                f"{weather['Humidity']}%"
            )

            col4.metric(
                "Wind Speed",
                f"{weather['Wind Speed']:.1f} m/s"
            )


            # --------------------------------------
            # Additional Weather Information
            # --------------------------------------

            st.markdown("### 📋 Additional Information")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "☁️ Condition",
                weather["Weather"]
            )

            col2.metric(
                "🌡️ Pressure",
                f"{weather['Pressure']} hPa"
            )

            col3.metric(
                "📝 Description",
                weather["Description"].title()
            )


# ==================================================
# MULTI-CITY WEATHER DASHBOARD
# ==================================================

st.markdown("---")

st.header("📊 Multi-City Weather Comparison")

st.write(
    "Compare current weather conditions across "
    "selected cities."
)


# ==================================================
# CITY LIST
# ==================================================

cities = [
    "Delhi",
    "Mumbai",
    "Kolkata",
    "Chennai",
    "Bangalore",
    "Hyderabad",
    "Bankura",
    "Durgapur"
]


# ==================================================
# REFRESH WEATHER DATA
# ==================================================

refresh_col1, refresh_col2 = st.columns(
    [5, 1]
)

with refresh_col2:

    refresh_clicked = st.button(
        "🔄 Refresh",
        use_container_width=True
    )


if refresh_clicked:

    get_weather.clear()

    st.rerun()


# ==================================================
# FETCH MULTI-CITY WEATHER DATA
# ==================================================

weather_data_list = []

failed_cities = []

with st.spinner(
    "Fetching weather data for selected cities..."
):

    for city_name in cities:

        result = get_weather(city_name)

        if result["success"]:

            weather_data_list.append(
                result["data"]
            )

        else:

            failed_cities.append(
                city_name
            )


# ==================================================
# CREATE DATAFRAME
# ==================================================

df = create_dataframe(
    weather_data_list
)

df = clean_data(df)


# ==================================================
# HANDLE EMPTY DATA
# ==================================================

if df.empty:

    st.error(
        "❌ No weather data available. "
        "Please check your API key or internet connection."
    )


else:

    # ==================================================
    # WEATHER DATA TABLE
    # ==================================================

    st.subheader("🌍 Current Weather Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    # ==================================================
    # FAILED CITY WARNING
    # ==================================================

    if failed_cities:

        st.warning(
            "Weather data could not be retrieved for: "
            + ", ".join(failed_cities)
        )


    # ==================================================
    # OVERALL WEATHER METRICS
    # ==================================================

    st.subheader("📌 Overall Weather Statistics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🌡️ Avg Temperature",
        f"{df['Temperature'].mean():.2f} °C"
    )

    col2.metric(
        "💧 Avg Humidity",
        f"{df['Humidity'].mean():.2f}%"
    )

    col3.metric(
        "💨 Avg Wind Speed",
        f"{df['Wind Speed'].mean():.2f} m/s"
    )

    col4.metric(
        "🌍 Cities Available",
        len(df)
    )


    # ==================================================
    # STATISTICAL SUMMARY
    # ==================================================

    st.subheader("📈 Statistical Summary")

    st.dataframe(
        df.describe(),
        use_container_width=True
    )


    # ==================================================
    # VISUALIZATIONS
    # ==================================================

    st.subheader("📊 Weather Visualizations")

    # Temperature / weather line chart
    line_chart(df)

    # Bar chart
    bar_chart(df)

    # Correlation heatmap
    heatmap(df)

    # Weather condition distribution
    pie_chart(df)


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "🌦️ Weather Information & Analytics App | "
    "Powered by OpenWeatherMap API"
)

st.caption(
    "Built with Python, Streamlit, Pandas, Matplotlib and Seaborn"
)