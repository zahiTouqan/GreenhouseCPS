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
import streamlit as st

chat_id = "5790406939"
bot_id = "6237670603:AAG7YRoBlpeyu9vNsEOJPQuvU1sGVvUoO9o"
GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

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

    humidity = st.empty()
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
        GPIO.output(16,GPIO.LOW)
        Mled = False
        TLed = False
        HLed = False
        LLed = False
        moistureState = None
        humiState = None
        tempState = None
        lightState = None

        #Moisture:
        m = test()
        maxval = 950 #max value of moisture in water
        per = (m / maxval) * 100
        if 0 <= m and m < 150:
            moistureState = 'Dry'
            GPIO.output(21, GPIO.LOW)  # Turn motor on
            if 0 <= m and m < 50:
                time.sleep(6)
            elif 50 <= m and m < 100:
                time.sleep(4)
            elif 100 <= m and m < 150:
                time.sleep(2)
            GPIO.output(21, GPIO.HIGH)  # Turn motor off
        elif 450 <= m:
            moistureState = 'Wet'
        #Temperature:
        humi, temp = dht.main()
        if temp < 16:
            tempState = 'Low'
        elif 26 < temp:
            tempState = 'High'
        #Humidity
        if humi < 40:
            humiState = 'Low'
        elif 70 < humi:
            humiState = 'High'
        if humiState is not None:
            if humiState == 'Low' or humiState == 'High':
                message += "The Humidity is Very {}: {}C\n".format(humiState, humi)
                HLed = True
		
        print('Humidity: {:.2f}'.format(humi))
	
        #Light:
        l = light.main()
        lightPer = (l / 1000) * 100
        if 0 <= l < 500:
            lightState = 'Dark'
        elif 700 > l:
            lightState = 'Bright'
        if lightPer < 50:
          color = "green"  # Green for lower values
        elif lightPer < 75:
          color = "orange"  # Orange for values between 50 and 75
        else:
          color = "red"
        display_humidity(humi, humidity, color)
        create_thermometer_widget(thermometer1_container, temp, 0, 100, "Temperature")
        create_thermometer_widget(thermometer2_container, lightPer, 0, 100, "Light")
        fig.update_traces(value=per)
        fig.update_traces(gauge={'bar': {'color': color}})
        gauge_container.plotly_chart(fig, use_container_width=True)

        if moistureState is not None:
            if moistureState == 'Wet' or moistureState == 'Dry':
                message = "Your Soil is Very {}: {:.2f}%\n".format(moistureState, per)
                MLed = True
                st.components.v1.html(
                    f"<script>alert('Threshold exceeded for Moisture, your soil is very {moistureState} : {per}');</script>")

        print('Percentage of Moisture: {:.2f}%'.format(per))
        if lightState is not None:
            if lightState == 'Dark' or lightState == 'Bright':
                message += "The Light Intensity is Too {}: {:.2f}%".format(lightState, lightPer)
                LLed = True
                st.components.v1.html(
                    f"<script>alert('Threshold exceeded for Moisture, your soil is very {lightState} : {lightPer}');</script>")

        print('Light Intensity: {0}'.format(l))
        if humiState is not None:
            if humiState == 'Low' or humiState == 'High':
                message += "The Humidity is Very {}: {}C\n".format(humiState, humi)
                HLed = True
                st.components.v1.html(
                    f"<script>alert('Threshold exceeded for Moisture, your soil is very {humiState} : {humi}');</script>")

        print('Humidity: {:.2f}'.format(humi))
        if tempState is not None:
            if tempState == 'Low' or tempState == 'High':
                message += "The Temperature is Very {}: {}C\n".format(tempState, temp)
                TLed = True
                st.components.v1.html(
                    f"<script>alert('Threshold exceeded for Moisture, your soil is very {tempState} : {temp}');</script>")

        print('Temperature: {0}'.format(temp))
        #Led Initial Response:
        if MLed or TLed or HLed or LLed:
            GPIO.output(16,GPIO.HIGH)

        #Telegram Warning Message
        if message is not None:
            url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
            print(requests.get(url).json())
        time.sleep(60)
        

if __name__ == "__main__":
    main()
