#import subprocess

#command = 'python moisture.py 0'
# m = test()
#p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#print("output:", p.stdout)
from moisture import test
import dht
import light
import requests
import RPi.GPIO as GPIO
import time

chat_id = "5790406939"
bot_id = "6237670603:AAG7YRoBlpeyu9vNsEOJPQuvU1sGVvUoO9o"

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
