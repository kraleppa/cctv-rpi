from gpiozero import Button, LED


class GpioController:
    def __init__(self, camera, button1_pin=21, led_pin=20):
        self.camera = camera
        # FIXME uncomment
        # self.led = LED(led_pin)
        # self.button1 = Button(button1_pin)
        # FIXME uncomment
        # self.button1.when_activated = self.button1_action

    def button1_action(self):
        self.camera.switch_face_detection()
    # FIXME uncomment
    # def switch_led(self, value):
    #     if value:
    #         self.led.on()
    #     else:
    #         self.led.off()
