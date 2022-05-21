import os

import RPi.GPIO as GPIO
from time import sleep


def switch_lights():
    lights_state = os.popen('kasa --alias "Bedroom Lights" state').read()
    lights_state_tokens = lights_state.split()
    lights_on_index = lights_state_tokens.index("state:") + 1
    lights_on = lights_state_tokens[lights_on_index] == "ON"
    lights_ip_index = lights_state_tokens.index("hostname") + 2
    lights_ip = lights_state_tokens[lights_ip_index]
    command = "on"
    if (lights_on): command = "off"
    os.system(f'kasa --host {lights_ip} {command}')


GPIO.setmode(GPIO.BCM)

sleep_time = 0.1

buttonPin = 17

GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

button_state = 0

try:
    while True:
        if button_state == 0:
            if (not GPIO.input(buttonPin)):
                button_state = 1
        if button_state == 1:
            if (GPIO.input(buttonPin)):
                button_state = 0
                switch_lights()
                sleep(sleep_time)
finally:
    GPIO.cleanup()
