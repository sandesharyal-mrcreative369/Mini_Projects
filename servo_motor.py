import RPi.GPIO as GPIO
import time

print("Started")

def initialize_servo(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    pwm = GPIO.PWM(pin, 50)   # 50Hz
    pwm.start(0)

    return pwm

def set_angle(pwm, angle):
    duty = angle / 18 + 2.5

    pwm.ChangeDutyCycle(duty)
    time.sleep(0.02)

def servo_motor(pwm):

    while True:

        # 0 -> 180
        for angle in range(0, 181, 5):
            set_angle(pwm, angle)

        # 180 -> 0
        for angle in range(180, -1, -5):
            set_angle(pwm, angle)

# -----------------------------------
# MAIN
# -----------------------------------

SERVO_PIN = 18

try:
    pwm = initialize_servo(SERVO_PIN)

    servo_motor(pwm)

except KeyboardInterrupt:
    print("Stopped")

finally:
    pwm.stop()
    GPIO.cleanup()