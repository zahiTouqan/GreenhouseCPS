import streamlit as st
import ssl
import certifi
from urllib.request import urlopen
import plotly.graph_objects as go
from moisture import test
import dht
import light
import requests
import RPi.GPIO as GPIO
import time


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

while True:
	m = test()
	maxval = 950 #max value of moisture in water
	percentage = m / maxval
	per = percentage * 100
	if 0 <= m and m < 150:
		state = 'Dry'
	elif 150 <= m and m < 450:
		GPIO.output(16,GPIO.LOW)
	else:
		state = 'Wet'
	if state == 'Wet' or state == 'Dry':
		GPIO.output(16,GPIO.HIGH)
		message = "Your Soil is Very {}: {:.2f}%\n".format(state, per)
		#print(requests.get(url).json())
	print('Percentage of Moisture: {:.2f}%'.format(per))
	
	humi, temp = dht.main()
	if 16 <= temp <= 26:
		GPIO.output(16,GPIO.LOW)
	elif temp < 16:
		state = 'Low'
	else:
		state = 'High'
	if state == 'Low' or state == 'High':
		GPIO.output(16,GPIO.HIGH)
		message += "The Temperature is Very {}: {}C\n".format(state, temp)
		#print(requests.get(url).json())
	print('Temperature: {0}'.format(temp))
	
	l = light.main()
	lightPer = (l / 1000) * 100
	if 0 <= l < 500:
		state = 'Dark'
	elif 500 <= l < 700:
		GPIO.output(16, GPIO.LOW)
	else:
		state = 'Bright'
	if state == 'Dark' or state == 'Bright':
		GPIO.output(16, GPIO.HIGH)
		message += "The Light Intensity is Too {}: {:.2f}%".format(state, temp)
	print('Light Intensity: {0}'.format(l))
	
	#if not messageMoist is None:
		#message
	#message = messageMoist + messageTemp + messageLight
	if not message is None:
		url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
		print(requests.get(url).json())
	time.sleep(5)
