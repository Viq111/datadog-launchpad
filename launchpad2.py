import pygame
import pygame.midi
import sys

class LightMode:
    ON    = 0
    BLINK = 1
    FADE  = 2

class LightColor:
    BLUE =    41
    GREEN =   18
    MAGENTA = 53
    ORANGE =   9
    PURPLE =  54
    RED =      5
    WHITE =    3
    YELLOW =  13

# Internal functions

__inited = False

def __init():
    "Check if pygame was not inited, and do it"
    if not __inited:
        init()

# Class

class Device():
    def __init__(self, id, name, in_, out_):
        self.id = id
        self.name = name
        self.in_ = bool(in_)
        self.out_ = bool(out_)

    def is_input(self):
        return self.in_

    def is_output(self):
        return self.out_

# Useful functions

def init():
    # Init pygame
    pygame.init()
    pygame.midi.init()
    __inited = True

def quit():
    pygame.midi.quit()
    pygame.quit()

def list_devices():
    "List all devices"
    __init()
    devices = []
    for i in range(pygame.midi.get_count()):
        info = pygame.midi.get_device_info(i)
        d = Device(i, info[1], info[2], info[3])
        devices.append(d)
    return devices

class Launchpad():
    def __init__(self, device_in=None, device_out=None):
        "Link to a new launchpad, autodetect in/out"
        devices = list_devices()
        if device_in is None:
            device_in = filter(lambda d: d.is_input(), devices)[0]

        if device_out is None:
            device_out = filter(lambda d: d.is_output(), devices)[0]

        self.in_ = pygame.midi.Input(device_in.id)
        self.out_ = pygame.midi.Output(device_out.id)

    def wait_input(self):
        "Block until the user press a button"
        while True:
            if self.in_.poll():
                result = self.in_.read(1)[0][0]
                # Check if we click a button and not release it
                if result[2] == 127:
                    return result[1]
            pygame.time.wait(10) # wait 10ms

    def led_on(self, led, color=LightColor.BLUE, mode=LightMode.ON):
        self.out_.note_on(led, velocity=color, channel=mode)

    def led_off(self, led):
        for i in range(3): # Turn all mode off
            self.out_.note_off(led, channel=i)


if __name__ == "__main__":
    init()
    print "^C to quit..."
    l = Launchpad()
    leds_on = []
    try:
        while True:
            button = l.wait_input()
            print "Button pressed:", button
            if button not in leds_on:
                l.led_on(button)
                leds_on.append(button)
            else:
                l.led_off(button)
                leds_on.remove(button)
    except KeyboardInterrupt:
        pass
    print "Bye!"
    quit()
