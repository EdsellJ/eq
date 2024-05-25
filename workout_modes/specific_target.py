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
from gpiozero import Button, TonalBuzzer
from gpiozero.tones import Tone
from drivers.lib import color_change, await_hit, get_hit

def blink_all(stop_event):
    while not stop_event.is_set():
        #turn all sensors green
        led_driver.set_all(Color(0, 40, 0))
        sleep(.4)
        led_driver.clear_all()
        if stop_event.is_set():
            break
        sleep(.4)

def specific_target():
    button1 = Button(5)
    button2 = Button(13)
    while button1.wait_for_press():
        sleep(.01)
    
    led_driver.set_all(Color(0, 40, 0))
    


try:
    specific_target()
    sensor_driver.stop()
    led_driver.clear_all()
    exit()

except KeyboardInterrupt:
    sensor_driver.stop()
    led_driver.clear_all()
    exit()

# Define buzzer in pin gpio pin 24
buzzer = TonalBuzzer(24)

#play buzzer
buzzer.play(Tone("A4"))
sleep(1)
buzzer.stop()
