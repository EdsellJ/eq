#Combination Force
'''
The Equalizer illuminates a sequence of LED target locations Green. The goal is
for the user to strike the target location with maximum force. The appropriate
color LED light will illuminate determined by the force applied, i.e. yellow, red,
or purple. The Equalizer will randomly choose (predetermined by us) different
combination locations and the amount of strikes per combination. After a brief
pause, random combinations continue. The user has the ability to increase or
decrease the speed of the combination workout.
'''
from common_imports import *
import common_imports
led_driver, sensor_driver = common_imports.setup_drivers()

