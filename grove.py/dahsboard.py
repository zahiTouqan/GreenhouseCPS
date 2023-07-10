import streamlit as st
import ssl
import certifi
from urllib.request import urlopen
import plotly.graph_objects as go

st.title("Readings")
st.text("")
st.markdown("#")
fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 270,
    domain = {'x': [0, 0.5], 'y': [0, 0.5]},
    title = {'text': "Moisture"}))


def create_thermometer(value, min_value, max_value,measurement):
    filled = int((value - min_value) / (max_value - min_value) * 100)
    empty = 100 - filled

    #st.write("Thermometer")
    thermometer_container = st.container()
    if measurement != "Temperature":
     thermometer_container.bar_chart([filled], height=400,width=50, use_container_width=False)
    else:
     thermometer_container.progress(filled)
    st.write(f"{measurement} {value}°")
# Example usage within Streamlit
#value = st.slider("Value", 0, 100, 50)
#min_value = st.number_input("Min Value", value=0)
#max_value = st.number_input("Max Value", value=100)
create_thermometer(35,0,100,"Temperature")
percentage = 49
st.markdown(f"<h1 style='font-size: 100px; text-align: center;'>{percentage}%</h1>", unsafe_allow_html=True)
st.markdown(f"<h1 style='font-size: 28px; text-align: center;'>Humidity</h1>", unsafe_allow_html=True)
col1, col2,col3,col4,col5,col6,col7 = st.columns(7)
with col1:
     st.plotly_chart(fig)
# Press the green button in the gutter to run the script.

with col6:
         create_thermometer(50,0,100,"Light")
