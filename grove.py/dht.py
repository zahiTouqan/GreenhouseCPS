import time
import seeed_dht
import RPi.GPIO as GPIO

def main():

    # for DHT11/DHT22
    sensor = seeed_dht.DHT("11", 18)
    # for DHT10
    # sensor = seeed_dht.DHT("10")
    GPIO.setup(16,GPIO.OUT)
    
    while True:
        humi, temp = sensor.read()
        if not humi is None:
            print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
        else:
            print('DHT{0}, humidity & temperature: {1}'.format(sensor.dht_type, temp))
        if 16 <= temp <= 26:
            GPIO.output(16,GPIO.LOW)
        else:
            GPIO.output(16,GPIO.HIGH)
        time.sleep(1)


if __name__ == '__main__':
    main()
