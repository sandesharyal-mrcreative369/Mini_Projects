#Imported Libraries
import RPI.GPIO as GPIO
import time

#Define Pins
Trig_Pin = 17
Echo_Pin = 27


#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(Trig_Pin, GPIO.IN)
GPIO.setup(Echo_Pin, GPIO.OUT)

#Ensure trigger pin is low when ultrasonic sensor is started
GPIO.output(Trig_Pin, GPIO.LOW)
time.sleep(2)


try:
    pass

except KeyboardInterrupt:
    print("Measurement stopped")
    GPIO.cleanup()