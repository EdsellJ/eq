#Specific Target
'''
The user can cycle through all the target locations and choose which target to
train on. The Target will illuminate a predetermined force pressure LED color
(Yellow, Red, or Purple). The user is then required to deliver the proper amount
of force pressure to the chosen target according to the LED color displayed. Once
the proper amount of force pressure has been received, the user will hear an
audible tone or beep indicating to the user that their goal has been achieved. The
target location LED will then reset to the original predetermined LED color so
the user can repeat the specific target training. The user can change the target
location as desired.
'''
from common_imports import *
import common_imports
led_driver, sensor_driver = common_imports.setup_drivers()