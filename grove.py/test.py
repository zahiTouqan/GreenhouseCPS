from moisture import test
import dht
import light
import requests
import RPi.GPIO as GPIO
import time

GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

chat_id = "5790406939"
bot_id = "6237670603:AAG7YRoBlpeyu9vNsEOJPQuvU1sGVvUoO9o"

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
	if moistureState is not None:
		if moistureState == 'Wet' or moistureState == 'Dry':
			message = "Your Soil is Very {}: {:.2f}%\n".format(moistureState, per)
			MLed = True
		
	print('Percentage of Moisture: {:.2f}%'.format(per))
	
	#Temperature:
	humi, temp = dht.main()
	if temp < 16:
		tempState = 'Low'
	elif 26 < temp:
		tempState = 'High'
	if tempState is not None:
		if tempState == 'Low' or tempState == 'High':
			message += "The Temperature is Very {}: {}C\n".format(tempState, temp)
			TLed = True
		
	print('Temperature: {0}'.format(temp))
	
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
	if lightState is not None:
		if lightState == 'Dark' or lightState == 'Bright':
			message += "The Light Intensity is Too {}: {:.2f}%".format(lightState, lightPer)
			LLed = True
		
	print('Light Intensity: {0}'.format(l))
	
	#Led Initial Response:
	if MLed or TLed or HLed or LLed:
		GPIO.output(16,GPIO.HIGH)

	#Telegram Warning Message
	if message is not None:
		url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"
		print(requests.get(url).json())
	time.sleep(60)
