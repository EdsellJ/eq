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

def combination_target():
    button1 = Button(5)
    button2 = Button(13)
    while button1.wait_for_press():
        sleep(.01)
    
    led_driver.set_all(Color(0, 40, 0))

    #wait for button 2 to be pressed   
    while not button2.is_pressed:
        sleep(.01)