# Servo Motor Control using Raspberry Pi 3A+

import RPi.GPIO as GPIO
import time

# Define Servo Pin
SERVO_PIN = 18

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN,GPIO.OUT)


#PWM Setup
pwm = GPIO.PWM(SERVO_PIN,50)  #servo motor works at 50Hz

#Start PWM
pwm.start(0)

try:
    while True:

        # 0° -> 180°
        for i in range(2,13):
            pwm.ChangeDutyCycle(i)

            time.sleep(0.4)

        # 180° -> 0°
        for j in range(12,1,-1):
            pwm.ChangeDutyCycle(j)

            time.sleep(0.5)


except KeyboardInterrupt:
    print("Measurement stopped")
    GPIO.cleanup()


