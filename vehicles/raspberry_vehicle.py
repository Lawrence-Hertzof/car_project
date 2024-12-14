from Interfaces.ground_vehicle import GroundVehicle

import RPi.GPIO as GPIO


class RaspberryVehicle(GroundVehicle):
    MODE: int = GPIO.BCM

    RIGHT_FORWARD: int
    RIGHT_BACKWARD: int

    LEFT_FORWARD: int
    LEFT_BACKWARD: int

    def _set_low(self, gpio_pins: list[int]) -> None:
        for gpio_pin in gpio_pins:
            GPIO.output(gpio_pin, GPIO.LOW)

    def init_controls_from_config(self, config: dict) -> None:
        self.MODE = config.get("mode", self.MODE)
        GPIO.setmode(self.MODE)  # GPIO.BCM or GPIO.BOARD
        try:
            self.RIGHT_FORWARD = config["right_forward"]
            self.RIGHT_BACKWARD = config["right_backward"]
            self.LEFT_FORWARD = config["left_forward"]
            self.LEFT_BACKWARD = config["left_backward"]
        except KeyError:
            raise ValueError(
                "Missing one of the following keys: 'right_forward', 'right_backward', 'left_forward', 'left_backward'"
            )
        for gpio_pin in [self.RIGHT_FORWARD, self.RIGHT_BACKWARD, self.LEFT_FORWARD, self.LEFT_BACKWARD]:
            GPIO.setup(gpio_pin, GPIO.OUT)

    def move_forward(self) -> None:
        GPIO.output(self.LEFT_FORWARD, GPIO.HIGH)
        GPIO.output(self.RIGHT_FORWARD, GPIO.HIGH)

    def move_backward(self) -> None:
        GPIO.output(self.LEFT_BACKWARD, GPIO.HIGH)
        GPIO.output(self.RIGHT_BACKWARD, GPIO.HIGH)

    def move_right(self) -> None:
        GPIO.output(self.RIGHT_FORWARD, GPIO.HIGH)
        GPIO.output(self.LEFT_BACKWARD, GPIO.HIGH)

    def move_left(self) -> None:
        GPIO.output(self.LEFT_FORWARD, GPIO.HIGH)
        GPIO.output(self.RIGHT_BACKWARD, GPIO.HIGH)

    def stop(self) -> None:
        self._set_low(
            [self.LEFT_FORWARD, self.RIGHT_FORWARD, self.LEFT_BACKWARD, self.RIGHT_BACKWARD]
        )

