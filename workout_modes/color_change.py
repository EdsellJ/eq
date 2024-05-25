#imports 
from rpi_ws281x import Color
from time import sleep
import common_imports
#led_driver, sensor_driver = common_imports.setup_drivers()

#function to run the hit color test
def color_change(led_drive, index, value):
    #if the last value in captured_values is 0, turn the first led red
    if value < .3:
        led_drive.set_ring_color(index, Color(0, 40, 0))
    elif value <.6:
        led_drive.set_ring_color(index, Color(40, 40, 0))
    elif value <.9:
        led_drive.set_ring_color(index, Color(40, 0, 0))
    else:
        led_drive.set_ring_color(index, Color(40, 0, 40))
    sleep(.7)
    led_drive.clear(index)

