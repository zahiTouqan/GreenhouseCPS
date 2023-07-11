import RPi.GPIO as GPIO
import time

channel = 21

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
GPIO.setup(16,GPIO.OUT)


def motor_on(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn motor on
    GPIO.output(16,GPIO.HIGH)


def motor_off(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn motor off
    GPIO.output(16,GPIO.LOW)


if __name__ == '__main__':
    try:
        motor_on(channel)
        time.sleep(5)
        motor_off(channel)
        time.sleep(5)
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
