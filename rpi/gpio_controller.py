"""
This file contains logic for RPi handling LED and Button
through GPIO.
"""
from gpiozero import Button, LED


class GpioController:
    def __init__(self, camera, button1_pin=21, button2_pin=16, led_pin=20):
        self.camera = camera

        self.led = LED(led_pin)
        self.button1 = Button(button1_pin)
        self.button2 = Button(button2_pin)

        self.button1.when_activated = self.button1_action
        self.button2.when_activated = self.button2_action

    # switch face detection (ON/OFF)
    def button1_action(self):
        self.camera.switch_face_detection()

    # save current frame on disk (via switching __save_photo__ flag)
    def button2_action(self):
        self.camera.set_save_photo_flag()

    # switch LED diode according to current settings. Pass __face_detection__ flag as parameter
    def switch_led(self, value):
        if value:
            self.led.on()
        else:
            self.led.off()
