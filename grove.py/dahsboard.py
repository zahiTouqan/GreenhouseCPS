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

chat_id = "5790406939"
bot_id = "6237670603:AAG7YRoBlpeyu9vNsEOJPQuvU1sGVvUoO9o"

import streamlit as st
import plotly.graph_objects as go
import time


def create_thermometer_widget(container, value, min_value, max_value, measurement):
    # Create the empty placeholders for the thermometer widget
    filled = int((value - min_value) / (max_value - min_value) * 100)
    if filled < 50:
        color = "#00ff00"  # Green for lower values
    elif filled < 75:
        color = "#ffa500"  # Orange for values between 50 and 75
    else:
        color = "#ff0000"
        # Update the existing thermometer widget
    thermometer_style = f"""
        <style>
            .thermometer {{
                width: 50px;
                height: 400px;
                background: linear-gradient(to bottom, #eee {100 - filled}%, {color} {100 - filled}%);
                border-radius: 10px;
                display: flex;
                flex-direction: column-reverse;
                justify-content: flex-end;
                align-items: center;
                padding: 10px;
                box-sizing: border-box;
                font-weight: bold;
                text-align: center;
            }}
        </style>
    """
    thermometer_html = f"""
        <div class="thermometer">
            {measurement} {value}°
        </div>
    """
    container.markdown(thermometer_style + thermometer_html, unsafe_allow_html=True)


def display_humidity(perc, container, color):
    container.markdown(f"<h1 style='font-size: 100px; text-align: center;color:{color}'>{perc}%</h1>",
                       unsafe_allow_html=True)
    # container.markdown(f"<h1 style='font-size: 28px; text-align: center;'>Humidity</h1>", unsafe_allow_html=True)


def main():
    # Set up the dashboard layout
    st.title("Plant Readings")
    st.markdown("<br><br>", unsafe_allow_html=True)

    light = st.empty()
    st.markdown(f"<h1 style='font-size: 28px; text-align: center;'>Humidity</h1>", unsafe_allow_html=True)
    # Define the column layout
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 3, 2, 2])

    # Create the empty placeholders for the widgets
    thermometer1_container = col1.empty()
    gauge_container = col4.empty()
    thermometer2_container = col6.empty()

    # Define the indicator figure
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=0,
        domain={'x': [0, 1], 'y': [0.5, 1]},
        title={'text': "Moisture %"}
    ))
    fig.update_traces()
    while True:
        m = test()
        maxval = 950  # max value of moisture in water
        percentage = m / maxval
        per = percentage * 100
        if 0 <= m and m < 150:
            state = 'Dry'
        elif 150 <= m and m < 450:
            GPIO.output(16, GPIO.LOW)
        else:
            state = 'Wet'
        if state == 'Wet' or state == 'Dry':
            GPIO.output(16, GPIO.HIGH)
            message = "Your Soil is Very {}: {:.2f}%\n".format(state, per)
            # print(requests.get(url).json())
        print('Percentage of Moisture: {:.2f}%'.format(per))

        humi, temp = dht.main()
        if 16 <= temp <= 26:
            GPIO.output(16, GPIO.LOW)
        elif temp < 16:
            state = 'Low'
        else:
            state = 'High'
        if state == 'Low' or state == 'High':
            GPIO.output(16, GPIO.HIGH)
            message += "The Temperature is Very {}: {}C\n".format(state, temp)
        # print(requests.get(url).json())
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
        if lightPer < 50:
          color = "green"  # Green for lower values
        elif lightPer < 75:
          color = "orange"  # Orange for values between 50 and 75
        else:
          color = "red"
        display_humidity(humi, light, color)
        create_thermometer_widget(thermometer1_container, temp, 0, 100, "Temperature")
        create_thermometer_widget(thermometer2_container, lightPer, 0, 100, "Light")
        fig.update_traces(value=per)
        fig.update_traces(gauge={'bar': {'color': color}})
        gauge_container.plotly_chart(fig, use_container_width=True)

        if per > 70:
         st.components.v1.html(f"<script>alert('Threshold exceeded for value: {per}');</script>")
        print('Light Intensity: {0}'.format(l))
        # if not messageMoist is None:
        # message
        # message = messageMoist + messageTemp + messageLight
        if not message is None:
            url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
            print(requests.get(url).json())
        time.sleep(60)
