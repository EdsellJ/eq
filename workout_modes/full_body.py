#Full Body 
'''
All target locations are illuminated Green at the same time. The goal is for the
user to turn all LED sensors Red as quickly as possible. This is a timed event.
'''
from common_imports import *
import common_imports
led_driver, sensor_driver = common_imports.setup_drivers()