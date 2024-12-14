import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
libs_path = os.path.join(current_dir, 'libs')
sys.path.insert(0, libs_path)

from flask import Flask, Response
from picamera2 import Picamera2
import cv2


# Initialize Flask app
app = Flask(__name__)

# Initialize Picamera2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

def generate_frames():
    """Generate frames from the Raspberry Pi camera."""
    while True:
        # Capture a frame
        frame = picam2.capture_array()  # Get the current frame as a NumPy array

        # Encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame as part of an MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Serve the video feed."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Serve the main page with the embedded video."""
    return '''
        <html>
        <head>
            <title>Raspberry Pi Camera Stream</title>
        </head>
        <body>
            <h1>Raspberry Pi Camera Stream</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
        </html>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
