from gpiozero import Button, LED


class GpioController:
    def __init__(self, button1_pin=21, led_pin=20):
        self.led = LED(led_pin)
        self.button1 = Button(button1_pin)

        self.button1.when_activated = self.button1_action

    def button1_action(self):
        self.led.toggle()
