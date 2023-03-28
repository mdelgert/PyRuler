#https://github.com/adafruit/Adafruit_CircuitPython_HID/releases
#https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.mouse.Mouse

import os
import board
from digitalio import DigitalInOut, Direction
import time
import touchio

import analogio
import usb_hid
from adafruit_hid.mouse import Mouse

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

mouse = Mouse(usb_hid.devices)

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

touches = [DigitalInOut(board.CAP0)]
for p in (board.CAP1, board.CAP2, board.CAP3):
    touches.append(touchio.TouchIn(p))

leds = []
for p in (board.LED4, board.LED5, board.LED6, board.LED7):
    led = DigitalInOut(p)
    led.direction = Direction.OUTPUT
    led.value = True
    time.sleep(0.25)
    leds.append(led)
for led in leds:
    led.value = False
    
cap_touches = [False, False, False, False]

def read_caps():
    t0_count = 0
    t0 = touches[0]
    t0.direction = Direction.OUTPUT
    t0.value = True
    t0.direction = Direction.INPUT
    # funky idea but we can 'diy' the one non-hardware captouch device by hand
    # by reading the drooping voltage on a tri-state pin.
    t0_count = t0.value + t0.value + t0.value + t0.value + t0.value + \
               t0.value + t0.value + t0.value + t0.value + t0.value + \
               t0.value + t0.value + t0.value + t0.value + t0.value
    cap_touches[0] = t0_count > 2
    cap_touches[1] = touches[1].raw_value > 3000
    cap_touches[2] = touches[2].raw_value > 3000
    cap_touches[3] = touches[3].raw_value > 3000
    return cap_touches

while True:
    caps = read_caps()
    #print(caps)
    # light up the matching LED
    for i,c in enumerate(caps):
        leds[i].value = c
    if caps[0]:
        print("1")
    if caps[1]:
        print("2")
    if caps[2]:
        print("3")
    if caps[3]:
        print("4")
        mouse.move(x=1)
        #layout.write('test')
    time.sleep(0.1)