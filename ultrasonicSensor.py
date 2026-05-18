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
    while True:

        #Generate Trigger Pulse
        GPIO.output(Trig_Pin, GPIO.HIGH)
        time.sleep(0.00005)  #50 Microseconds

        GPIO.output(Trig_Pin, GPIO.LOW)
        time.sleep(0.00002)   #20 Microseconds


        #Measure Echo Pulse
        while GPIO.input(Echo_Pin) == GPIO.LOW:
            pulse_start = time.time()

        while GPIO.input(Trig_Pin) == GPIO.HIGH:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

except KeyboardInterrupt:
    print("Measurement stopped")
    GPIO.cleanup()