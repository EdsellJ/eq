#Warmup 
'''
All 34 LED target locations are randomly illuminated green, one at a time. The
LED light will stay green until struck. Once the user strikes the target location,
that LED light will go out and another light at a random location will illuminate
green until struck and so on, for 60 seconds.
'''
from common_imports import *
import common_imports
led_driver, sensor_driver = common_imports.setup_drivers()