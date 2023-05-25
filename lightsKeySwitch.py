import os
from pynput import keyboard

class Lights:
    def __init__(self, lights_name):
        self.name = lights_name
        self.button_state = 0
        lights_state = os.popen(f'kasa --alias "{lights_name}" state').read()
        lights_state_tokens = lights_state.split()
        lights_ip_index = lights_state_tokens.index("hostname") + 2
        
        self.lights_ip = lights_state_tokens[lights_ip_index]
        
    def switch(self):
        switch_lights(self.lights_ip)
            
def switch_lights(lights_ip):
    lights_state = os.popen(f'kasa --host "{lights_ip}" state').read()
    lights_state_tokens = lights_state.split()
    lights_on_index = lights_state_tokens.index("state:") + 1
    lights_on = lights_state_tokens[lights_on_index] == "True"

    command = "on"
    if (lights_on): command = "off"
    os.system(f'kasa --host {lights_ip} {command}')

def switch_lights_by_name(lights_name):
    lights_state = os.popen(f'kasa --alias "{lights_name}" state').read()
    lights_state_tokens = lights_state.split()
    lights_ip_index = lights_state_tokens.index("hostname") + 2
    lights_ip = lights_state_tokens[lights_ip_index]
    switch_lights(lights_ip)


if __name__ == "__main__":
    bedroom_lights = Lights("Bedroom Lights")

    def switch_light_on_key_release(key):
        if key == keyboard.Key.pause:
            bedroom_lights.switch()

    with keyboard.Listener(on_release = switch_light_on_key_release) as listener:
        listener.join()
