import cv2
import socket
import threading
from flask import Flask, Response, render_template_string
from ultralytics import YOLO
import math
import time
import cvzone


# -----------------------------------------
# GLOBAL VARIABLES
# -----------------------------------------
current_distance = 0.0
PI_IP = 'Your Raspberry Pi address'
PORT = 5001
person_count = 0


#Yolo Model
model = YOLO('yolov8n.pt')

# Load built-in class names from YOLO model
classNames = model.names

#Object creation for Flask server
app = Flask(__name__)


# -----------------------------------------
# SOCKET CLIENT THREAD (Background Task)
# -----------------------------------------
def receive_distance():
    global current_distance

    while True:

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to Raspberry Pi at {PI_IP}:{PORT}...")

        try:
            #Retrying connection every 5 seconds
            client.settimeout(5)
            client.connect((PI_IP, PORT))
            client.settimeout(None)
            print("Connected to Pi successfully!")

            while True:
                #Receiving data from server
                data = client.recv(1024).decode()

                if not data:
                    print("Connection closed by the Pi.")
                    break

                try:
                    current_distance = float(data)
                except ValueError:
                    pass

        except Exception as e:
            print(f"Socket Error: {e}")
            current_distance = 0.0


        print("Retrying connection in 3 seconds...")
        time.sleep(3)



# -----------------------------------------
# YOLO & CAMERA STREAMING
# -----------------------------------------
def generate_frames():
    global current_distance, person_count

    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()

        # RESET PERSON COUNT EVERY FRAME
        person_count = 0
        if not success:
            break

        result = model(frame, stream=True)

        # PROCESS YOLO RESULTS
        for r in result:
            boxes = r.boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]  # Get bounding box coordinates
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert float -> int
                w, h = x2 - x1, y2 - y1  # WIDTH AND HEIGHT

                # DRAW CORNER RECTANGLE
                cvzone.cornerRect(frame, (x1, y1, w, h), l=10, t=1)

                # Detection confidence
                confidence = math.ceil(box.conf[0] * 100) / 100

                # Get className
                cls = int(box.cls[0])
                class_classified = classNames[cls]

                # 1. CHECK INSIDE THE LOOP FOR EACH OBJECT DETECTED
                if class_classified == "person" and confidence > 0.3:
                    # 2. CHECK DISTANCE FOR THE PERSON
                    if current_distance > 0 and current_distance <= 150:
                        person_count += 1

        # 3. DECIDE ALERT OR SAFE AFTER CHECKING ALL BOXES IN THE FRAME
        if person_count > 0:

            status_color = (0, 0, 255)  # Red Color for Alert
            alert_msg = "ALERT: Person in Zone!"
            cv2.putText(frame, alert_msg, (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 3)

        else:

            status_color = (0, 255, 0)  # Green Color for Safe
            cv2.putText(frame, "SAFE: Out of Range", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 3)


        # DISPLAY DISTANCE AND COUNT
        cv2.putText(frame, f"Distance: {current_distance:.1f} cm", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        cv2.putText(frame, f"Person Count: {person_count}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)


        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Flask yield function for returning the frames
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')




# -----------------------------------------
# FLASK WEB ROUTES
# -----------------------------------------
@app.route('/')
def index():

    #Creation of webpage using HTML
    html = """
    <html>
        <head><title>YOLO + Ultrasonic Stream</title></head>
        <body style="text-align: center; background-color: black; color: white;">
            <h1>Live Detection Stream</h1>
            <img src="/video_feed" width="800" style="border: 2px solid white;"/>
        </body>
    </html>
    """
    return render_template_string(html)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# -----------------------------------------
# MAIN EXECUTION
# -----------------------------------------
if __name__ == '__main__':

    #Using thread for Parallel Processing
    socket_thread = threading.Thread(target=receive_distance, daemon=True)
    socket_thread.start()


    print("Starting Flask Server... Open http://127.0.0.1:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=False)
    #Host 0.0.0.0 is to connect any Network IP address for Flask