import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
libs_path = os.path.join(current_dir, 'libs')
sys.path.insert(0, libs_path)

import RPi.GPIO as GPIO
from flask import Flask, Response, request
from picamera2 import Picamera2
import cv2

# GPIO Pin Setup
LEFT_WHEEL_FORWARD = 26
LEFT_WHEEL_BACKWARD = 19
RIGHT_WHEEL_FORWARD = 13
RIGHT_WHEEL_BACKWARD = 6


GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_WHEEL_FORWARD, GPIO.OUT)
GPIO.setup(RIGHT_WHEEL_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_WHEEL_BACKWARD, GPIO.OUT)
GPIO.setup(RIGHT_WHEEL_BACKWARD, GPIO.OUT)

def move_forward(command: bool) -> None:
    if command:
        GPIO.output(LEFT_WHEEL_FORWARD, GPIO.HIGH)
        GPIO.output(RIGHT_WHEEL_FORWARD, GPIO.HIGH)
    else:
        GPIO.output(LEFT_WHEEL_FORWARD, GPIO.LOW)
        GPIO.output(RIGHT_WHEEL_FORWARD, GPIO.LOW)

def move_backward(command: bool) -> None:
    if command:
        GPIO.output(LEFT_WHEEL_BACKWARD, GPIO.HIGH)
        GPIO.output(RIGHT_WHEEL_BACKWARD, GPIO.HIGH)
    else:
        GPIO.output(LEFT_WHEEL_BACKWARD, GPIO.LOW)
        GPIO.output(RIGHT_WHEEL_BACKWARD, GPIO.LOW)

def move_right(command: bool) -> None:
    if command:
        GPIO.output(RIGHT_WHEEL_FORWARD, GPIO.HIGH)
        GPIO.output(LEFT_WHEEL_BACKWARD, GPIO.HIGH)
    else:
        GPIO.output(RIGHT_WHEEL_FORWARD, GPIO.LOW)
        GPIO.output(LEFT_WHEEL_BACKWARD, GPIO.LOW)

def move_left(command: bool) -> None:
    if command:
        GPIO.output(LEFT_WHEEL_FORWARD, GPIO.HIGH)
        GPIO.output(RIGHT_WHEEL_BACKWARD, GPIO.HIGH)
    else:
        GPIO.output(LEFT_WHEEL_FORWARD, GPIO.LOW)
        GPIO.output(RIGHT_WHEEL_BACKWARD, GPIO.LOW)


# Initialize Flask app
app = Flask(__name__)

# Initialize Picamera2
picam2 = Picamera2()
# 1280x720
# camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
camera_config = picam2.create_preview_configuration(main={"size": (1280, 720)})
picam2.configure(camera_config)
picam2.start()


def _preprocess_frame(frame):
        flipped_frame = cv2.flip(frame, -1)
        corrected_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
        return corrected_frame


def generate_frames():
    """Generate frames from the Raspberry Pi camera."""
    while True:
        frame = picam2.capture_array()  # Get the current frame as a NumPy array
        # flipped_frame = cv2.flip(frame, -1)
        # # Convert from BGR to RGB
        # corrected_image = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
        processed_frame = _preprocess_frame(frame)
        # Encode frame to JPEG
        _, buffer = cv2.imencode('.jpg', processed_frame)
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
    # """Serve the main page with video and control buttons."""
    # return '''
    #     <html>
    #     <head>
    #         <title>Raspberry Pi Car</title>
    #     </head>
    #     <body>
    #         <h1>Raspberry Pi Car Control</h1>
    #         <img src="/video_feed" width="1280" height="720">
    #         <br>
    #         <button onclick="sendCommand('forward')">Forward</button>
    #         <button onclick="sendCommand('backward')">Backward</button>
    #         <button onclick="sendCommand('right')">RIGHT</button>
    #         <button onclick="sendCommand('left')">LEFT</button>
    #         <button onclick="sendCommand('stop')">Stop</button>
    #         <script>
    #             function sendCommand(command) {
    #                 fetch(`/control?command=${command}`);
    #             }
    #         </script>
    #     </body>
    #     </html>
    # '''
        # """Serve the main page with video and control buttons."""
    return """
        <html>
        <head>
            <title>Raspberry Pi Car</title>
            <style>
    body {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        margin: 0;
        font-family: Arial, sans-serif;
    }

    h1 {
        margin-bottom: 20px;
    }

    img {
        max-width: 90%;
        height: auto;
        border: 2px solid #000;
    }

    .controls {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        margin-top: 20px;
    }

    .horizontal {
        display: flex;
        gap: 10px;
    }

    button {
        background: none;
        border: none;
        cursor: pointer;
        padding: 10px;
    }

    button img {
        width: 50px;
        height: 50px;
    }
</style>

        </head>
        <body>
            <h1>Raspberry Pi Car Control</h1>
            <img src="/video_feed" width="1280" height="720">
            <br>
            <div></div>
            <div class="controls">
                <button onmousedown="sendCommand('forward')" onmouseup="sendCommand('stop')">
                    <img src="/static/arrow-up.png" alt="Forward">
                </button>
                <div class="horizontal">
                    <button onmousedown="sendCommand('left')" onmouseup="sendCommand('stop')">
                        <img src="/static/arrow-left.png" alt="Left">
                    </button>
                    <button onmousedown="sendCommand('right')" onmouseup="sendCommand('stop')">
                        <img src="/static/arrow-right.png" alt="Right">
                    </button>
                </div>
                <button onmousedown="sendCommand('backward')" onmouseup="sendCommand('stop')">
                    <img src="/static/arrow-down.png" alt="Backward">
                </button>
            </div>
            <script>
                function sendCommand(command) {
                    fetch(`/control?command=${command}`);
                }
            </script>
        </body>
        </html>
    """


@app.route('/control')
def control():
    """Handle control commands."""
    command = request.args.get('command')
    if command == 'forward':
        move_backward(False) # In case we moved backward just before
        move_forward(True)
    elif command == 'backward':
        move_forward(False) # In case we moved forward just before
        move_backward(True)
    elif command == 'right':
        move_left(False)
        move_right(True)
    elif command == 'left':
        move_right(False)
        move_left(True)
    elif command == 'stop':
        move_right(False)
        move_left(False)
        move_forward(False)
        move_backward(False)
    return '', 204

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()
