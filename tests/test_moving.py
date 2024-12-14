import RPi.GPIO as GPIO
import time

LEFT_WHEEL_FORWARD = 26
LEFT_WHEEL_BACKWARD = 19


RIGHT_WHEEL_FORWARD = 13
RIGHT_WHEEL_BACKWARD = 6

GPIO.setmode(GPIO.BCM)

# LEFT WHEEL
GPIO.setup(LEFT_WHEEL_FORWARD, GPIO.OUT)
GPIO.setup(LEFT_WHEEL_BACKWARD, GPIO.OUT)
# RIGHT WHEEL
GPIO.setup(RIGHT_WHEEL_FORWARD, GPIO.OUT)
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
        

if __name__ == "__main__":

    print("Running LEFT FORWARD WHEEL")
    GPIO.output(LEFT_WHEEL_FORWARD, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LEFT_WHEEL_FORWARD, GPIO.LOW)
    
    print("Running LEFT WHEEL BACKWARD")
    GPIO.output(LEFT_WHEEL_BACKWARD, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LEFT_WHEEL_BACKWARD, GPIO.LOW)

    print("Running RIGHT FORWARD WHEEL")
    GPIO.output(RIGHT_WHEEL_FORWARD, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(RIGHT_WHEEL_FORWARD, GPIO.LOW)


    print("Running RIGHT WHEEL BACKWARD")
    GPIO.output(RIGHT_WHEEL_BACKWARD, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(RIGHT_WHEEL_BACKWARD, GPIO.LOW)

    
    # GPIO.output(RIGHT_WHEEL_FORWARD, GPIO.HIGH)
    # for x in range(3):
    #     move_forward(True)
    #     time.sleep(2)
    #     move_forward(False)
    #     time.sleep(2)
    #     move_backward(True)
    #     time.sleep(2)
    #     move_backward(False)

    GPIO.cleanup()
