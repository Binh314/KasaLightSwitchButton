import os

import RPi.GPIO as GPIO
from time import sleep

class Lights:
    def __init__(self, lights_name, button_pin):
        self.name = lights_name
        self.button_pin = button_pin
        self.button_state = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
    def update(self):
        if self.button_state == 0:
            if (not GPIO.input(self.button_pin)):
                self.button_state = 1
        if self.button_state == 1:
            if (GPIO.input(self.button_pin)):
                self.button_state = 0
                switch_lights(self.name)

def switch_lights(lights_name):
    lights_state = os.popen(f'kasa --alias "{lights_name}" state').read()
    lights_state_tokens = lights_state.split()
    lights_on_index = lights_state_tokens.index("state:") + 1
    lights_on = lights_state_tokens[lights_on_index] == "ON"
    lights_ip_index = lights_state_tokens.index("hostname") + 2
    lights_ip = lights_state_tokens[lights_ip_index]
    command = "on"
    if (lights_on): command = "off"
    os.system(f'kasa --host {lights_ip} {command}')


if __name__ == "__main__":
    
    while True: # restart if any errors
    
        try:
            # initialize lights here
            bedroom_lights = Lights("Bedroom Lights", 17)
            kitchen_lights = Lights("Kitchen Lights", 26)
        
            # add lights here
            all_lights = [bedroom_lights, kitchen_lights]

            try:
                while True:
                    for lights in all_lights:
                        lights.update();
            finally:
                GPIO.cleanup()
            
        except:
            print("Restarting...")
        
        sleep(5)
        

