import streamlit as st
import plotly.express as px
from backend import get_data

def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

st.title("Weather Forecast for upto Next 5 Days")
place = st.text_input("City Name: ")
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days")
data_type = st.selectbox("Select the data to view", ("Temperature", "Sky-condition"))

if not place:
    st.subheader("Enter a city name to get started")

else:
    weather_data = get_data(place, days, data_type)
    if weather_data == "not_found":
        st.subheader(f"City \"{place}\" not found! Enter a valid city name.")

    else:
        dates = weather_data['dt']
        data = weather_data['data']
        st.subheader(f"{data_type} for the next {days} days in {place}")

        if data_type == "Temperature":
            figure = px.line(x=dates, y=data, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        elif data_type == "Sky-condition":
            chunk_size = 4
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}
            for chunk in chunk_data(list(zip(data, dates)), chunk_size):
                cols = st.columns(chunk_size)
                for i, (condition, date) in enumerate(chunk):
                    with cols[i]:
                        st.image(images[condition], width=130)
                        st.text(date.replace(" ", " | "))