# common_imports.py
from time import sleep
import time
import random
import threading
from rpi_ws281x import Color
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from drivers.ringctl import LEDRingDriver
from drivers.filmsense import FilmSensor

def setup_drivers():
    with open('config.json') as f:
        data = json.load(f)
        num_rings = data['num_rings']
        leds_per_ring = data['leds_per_ring']
        num_sensors = data['num_sensors']

        led_driver = LEDRingDriver(num_rings, leds_per_ring)
        sensor_driver = FilmSensor(num_sensors)
        return led_driver, sensor_driver