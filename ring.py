#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import PixelStrip, Color
import argparse
import RPi.GPIO as GPIO
from time import sleep
import random
#import function to capture filmsensor values
from filmsense import capture

RINGS = {0: 0, 1: 8, 2: 16, 3: 17}

GPIO.setmode(GPIO.BOARD)

GPIO.setup(3, GPIO.IN)

# LED strip configuration:
LED_COUNT = 24        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Define functions which animate LEDs in various ways
def colorClear(strip):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))
        strip.show()

def colorWipe(strip, color, ring_number):
    """Wipe color across display a pixel at a time."""
    #set the starting led
    start = RINGS[ring_number]
    if ring_number in {0, 1, 2}:
        end = RINGS[ring_number+1]
        for i in range(end-start):
            led = i + start
            strip.setPixelColor(led, color)
            strip.show()
            time.sleep(5 / 1000.0)
    else:
        for i in range(8):
            led = i + start
            strip.setPixelColor(led, color)
            strip.show()
            time.sleep(5/1000.0)

def sense(strip, sensor, ring):
    try:
        prevFunction = None
        while True:
            #turn strip white
            colorWipe(strip, Color(0, 255, 0), ring)
            sensor_value = capture(sensor) #run capture function and await the result
            
            #if-else to determine what color to turn the led's
            if sensor_value < .8:
                colorWipe(strip, Color(255, 255, 0), ring) #yellow
                break

            elif sensor_value < .9:
                colorWipe(strip, Color(255, 0, 0), ring) #red
                break

            else:
                colorWipe(strip, Color(255, 0, 100), ring) #purple
                break

            sleep(1)


    except KeyboardInterrupt:
        if args.clear:
            colorClear(strip)

def warmup(strip):
    try:
        prevFunction = None
        while True:
            Randnumber = random.randint(0, 2)
            sense(strip, Randnumber, Randnumber)
            time.sleep(.08)
            colorWipe(strip, Color(0,0,0), Randnumber)
    except KeyboardInterrupt:
        if args.clear:
            colorClear(strip)
            # Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    warmup(strip)
    """
    while True:
        colorWipe(strip, Color(0, 255, 0), 1)
        time.sleep(1) 
        colorWipe(strip, Color(0, 0, 0), 1)
        colorWipe(strip, Color(0, 255, 0), 2)
        time.sleep(1)
        colorWipe(strip, Color(0, 0, 0), 2)
    """



    
