#This is the code for Raspberry pi as a server
import socket
import time
from ultrasonic import *

# -----------------------------------------------
# Note:
# This code is run on Raspberry Pi Side(Server)
# ----------------------------------------------

# -----------------------------------------
# ULTRASONIC
# -----------------------------------------
TRIG_PIN = 12
ECHO_PIN = 13

#Intializing the ultrasonic sensor
initialize_ultrasonic(TRIG_PIN, ECHO_PIN)

# -----------------------------------------
# SOCKET SERVER
# -----------------------------------------

#To access Flask server from any network IP address
HOST = '0.0.0.0'
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(1)

print(f"Server started on port {PORT}. Waiting for laptop connection...")

while True:
    try:
        conn, addr = server.accept()
        print(f"Connected to: {addr}")

        # -----------------------------------------
        # SEND DISTANCE
        while True:
            #Generating the pulse
            pulse = generate_pulse(TRIG_PIN, ECHO_PIN)

            #Calculating the distance
            distance = calculate_distance(pulse)

            data = str(distance)

            #Sends the data to client
            conn.send((data + "\n").encode())

            time.sleep(0.1)

    except (BrokenPipeError, ConnectionResetError):
        print("Connection lost. Waiting for a new connection...")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:

        try:
            conn.close()
        except NameError:
            pass
