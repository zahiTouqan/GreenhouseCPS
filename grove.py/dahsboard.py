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

chat_id = ""
bot_id = ""
GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

def create_thermometer_widget(container, value, min_value, max_value, measurement,color):
    # Create the empty placeholders for the thermometer widget
    filled = int((value  / max_value) * 100)
    x = "°" 
    if measurement == "Light":
      x = "%"
        # Update the existing thermometer widget
    thermometer_style = f"""
        <style>
            .{measurement} {{
                width: 50px;
                height: 400px;
                background: linear-gradient(to bottom, #eee {100 - filled:.2f}%, {color} {100 - filled:.2f}%);
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
        <div class={measurement}>
            {measurement} {value:.2f}{x}
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
    #st.markdown(f"""<style> p {background-image: url(‘/home/cch/Downloads/LocalRepo/GreenhouseCPS/grove.py/094ebaba58c0194445812ad1b4552f9a-1484388571’);}</style>""",unsafe_allow_html=True)
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
        MLed = False
        TLed = False
        HLed = False
        LLed = False
        moistureState = None
        humiState = None
        tempState = None
        lightState = None
        lightColor = "green"
        humidityColor= "green"
        moistureColor= "green"
        tempColor = "green"
        message = ""
        
        #Moisture:
        m = test()
        maxval = 2500 #max value of moisture in water 0 - 1500: Dry, 1500 - 2000: Moist, 2000 - 2500: Wet 
        per = (m / maxval) * 100
        if 0 <= m and m < 150:
            moistureState = 'Dry'
            GPIO.output(21, GPIO.LOW)  # Turn motor on
            if 0 <= m and m < 500:
                time.sleep(6)
            elif 500 <= m and m < 1000:
                time.sleep(4)
            elif 1000 <= m and m < 1500:
                time.sleep(2)
            GPIO.output(21, GPIO.HIGH)  # Turn motor off
            moistureColor = "red"
        elif 2000 <= m:
            moistureState = 'Wet'
            moistureColor = "red"
        #Temperature:
        humi, temp = dht.main()
        if temp < 16:
            tempState = 'Low'
        elif 30 < temp:
            tempState = 'High'
            
        #Humidity
        if humi < 40:
            humiState = 'Low'
        elif 70 < humi:
            humiState = 'High'
        if humiState is not None:
            humidityColor = "red"
        if tempState is not None:
            tempColor = "red"
	
        #Light:
        l = light.main()
        lightPer = (l / 1000) * 100
        if 0 <= l < 500:
            lightState = 'Dark'
        elif 750 < l:
            lightState = 'Bright'
        if lightState is not None:
            lightColor = "red"
        display_humidity(humi, humidity, humidityColor)
        create_thermometer_widget(thermometer1_container, temp, 0, 50, "Temperature",tempColor)
        create_thermometer_widget(thermometer2_container, lightPer, 0, 100, "Light",lightColor)
        fig.update_traces(value=per)
        fig.update_traces(gauge={'bar': {'color': moistureColor}})
        gauge_container.plotly_chart(fig, use_container_width=True)

        if moistureState is not None:
            if moistureState == 'Wet' or moistureState == 'Dry':
                message += "Your Soil is Very {}: {:.2f}%\n".format(moistureState, per)
                MLed = True
                st.components.v1.html(
                    f"<script>alert('Threshold exceeded for Moisture: {moistureState} : {per:.2f}');</script>")

        print('Percentage of Moisture: {:.2f}%'.format(per))
        if lightState is not None:
            if lightState == 'Dark' or lightState == 'Bright':
                message += "The Light Intensity is Too {}: {:.2f}%".format(lightState, lightPer)
                LLed = True
                st.components.v1.html(
                    f"<script>alert('Threshold exceeded for Light: {lightState} : {lightPer:.2f}');</script>")

        print('Light Intensity: {0}'.format(l))
        if humiState is not None:
            if humiState == 'Low' or humiState == 'High':
                message += "The Humidity is Very {}: {}C\n".format(humiState, humi)
                HLed = True
                st.components.v1.html(
                    f"<script>alert('Threshold exceeded for Humidity: {humiState} : {humi}');</script>")

        print('Humidity: {:.2f}'.format(humi))
        if tempState is not None:
            if tempState == 'Low' or tempState == 'High':
                message += "The Temperature is Very {}: {}C\n".format(tempState, temp)
                TLed = True
                st.components.v1.html(
                    f"<script>alert('Threshold exceeded for Temperature: {tempState} : {temp}');</script>")

        print('Temperature: {0}'.format(temp))
        #Led Initial Response:
        if MLed or TLed or HLed or LLed:
            GPIO.output(16,GPIO.HIGH)

        #Telegram Warning Message
        if message is not "":
            url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
            print(requests.get(url).json())
        time.sleep(60)
        

if __name__ == "__main__":
    main()
