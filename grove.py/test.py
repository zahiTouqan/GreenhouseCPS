#import subprocess

#command = 'python moisture.py 0'
# m = test()
#p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#print("output:", p.stdout)
from moisture import test
import dht
import light
import RPi.GPIO as GPIO
import time
while True:
	m = test()
	maxval = 950 #max value of moisture in water
	percentage = m / maxval
	per = percentage * 100
	print('Percentage of Moisture: {:.2f}%'.format(per))
	
	humi, temp = dht.main()
	print('Temperature: {0}'.format(temp))
	
	l = light.main()
	print('Light Intensity: {0}'.format(l))
	time.sleep(5)
