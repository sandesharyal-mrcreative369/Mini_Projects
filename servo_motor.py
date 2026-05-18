# Servo Motor Control using Raspberry Pi 3A+

import RPi.GPIO as GPIO
import time

# Define Servo Pin
SERVO_PIN = 18

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN,GPIO.OUT)



