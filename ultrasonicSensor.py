import RPi.GPIO as GPIO
import time

# -------------------------------
# FUNCTION: Initialize Ultrasonic
# -------------------------------
def initialize_ultrasonic(trigger_pin, echo_pin):

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    # Ensure trigger pin is LOW
    GPIO.output(trigger_pin, False)

    print("Ultrasonic Sensor Initialized")
    time.sleep(2)


# -------------------------------
# FUNCTION: Generate Pulse
# -------------------------------
def generate_pulse(trigger_pin, echo_pin):

    # Send 10 microsecond pulse
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)

    pulse_start = time.time()
    pulse_end = time.time()

    timeout = time.time()

    # Wait for echo start
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()

        if pulse_start - timeout > 0.05:
            return None

    # Wait for echo end
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

        if pulse_end - timeout > 0.05:
            return None

    pulse_duration = pulse_end - pulse_start

    return pulse_duration


# -------------------------------
# FUNCTION: Calculate Distance
# -------------------------------
def calculate_distance(pulse_duration):

    if pulse_duration is None:
        return None

    # Speed of sound = 34300 cm/s
    distance = pulse_duration * 17150

    distance = round(distance, 2)

    return distance


# -------------------------------
# MAIN PROGRAM
# -------------------------------

TRIG_PIN = 12
ECHO_PIN = 13

initialize_ultrasonic(TRIG_PIN, ECHO_PIN)

try:

    while True:

        pulse = generate_pulse(TRIG_PIN, ECHO_PIN)

        distance = calculate_distance(pulse)

        if distance is not None:
            print(f"Distance: {distance} cm")
        else:
            print("Timeout Occurred")

        time.sleep(0.5)

except KeyboardInterrupt:

    print("Program Stopped")

    GPIO.cleanup()
