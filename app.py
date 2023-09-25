import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

# Path to your video file
# video_path = 'static/vid/vid.mp4'

# stream video 
# cap = cv2.VideoCapture(video_path)

# Initialize the webcam
cap = cv2.VideoCapture(0)


def generate_frames():
    while True:
        # Read a frame from the webcam
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
