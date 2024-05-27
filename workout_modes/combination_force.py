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
'''
Notes: On this one I am not sure how to increase the speed
'''
from random import randint
from common_imports import *
import common_imports
led_driver, sensor_driver = common_imports.setup_drivers()


from gpiozero import Button, TonalBuzzer
from gpiozero.tones import Tone
from drivers.lib import color_change, await_hit, get_hit

#setup button
button1 = Button(5)
button2 = Button(13)
#class to handdle button exception

exit_event = threading.Event()
button_pressed = 0
button_timer = 0

def set_button_pressed():
    global exit_event
    exit_event.set()
    print("exit event set")
    #set time button was pressed
    button_timer = time.time()

def button1_pressed():
    #exit function if button timer was pressed within the last second
    if time.time() - button_timer < 1:
        return
    while (button1.is_pressed):
        sleep(.01)
    global button_pressed
    button_pressed = 1
    print("button 1 pressed")
    set_button_pressed()

def button2_pressed():
    #exit function if button timer was pressed within the last second
    if time.time() - button_timer < 1:
        return
    global button_pressed
    button_pressed = 2
    print("button 2 pressed")
    set_button_pressed()

button1.when_pressed = button1_pressed
button2.when_pressed = button2_pressed

def combinations():
    #create lists of combinations and number of strikes
    combinations = [[1, 2, 1], [3, 5, 2], [2, 3, 2], [6, 4, 5], [7, 6, 0]]
    #randomly choose a combination
    combination = combinations[randint(0, len(combinations) - 1)]
    return combination

def flash_combination(combination):
    #flash the combination
    for i in combination:
        print("index: ", i)
        led_driver.set_ring_color(i , Color(0, 40, 0))
        sleep(.4)
        led_driver.clear(i)
        sleep(.4)

def combination_force():
    global button_pressed
    global exit_event
    #reset button_pressed and exit_event
    button_pressed = 0
    exit_event.clear()
    #run the combination
    #blink the lights in the combination order
    combo = combinations()
    print(combo)
    flash_combination(combo)
    #delay before lighting up current target
    sleep(.5)
    #light up the current target
    #setting up in a for loop in case combos are smaller or larger than 3
    for i in range(len(combo)):
        sensor_driver.start(combo[i])
        led_driver.set_ring_color(combo[i], Color(0, 40, 0))
        #wait for a hit
        await_hit(sensor_driver, exit_event)
        #if the user hit the reset button, continue to the next combination
        if exit_event.is_set():
            sensor_driver.stop()
            led_driver.clear_all()
            break
        #if hit, light up the target the appropriate color
        #get the hit
        sense, force = get_hit(sensor_driver)
        #change color in a thread
        threading.Thread(target=color_change, args=(led_driver, sense, force)).start()
        #stop drivers
        sensor_driver.stop()


#blink all sensors green
def blink_all(stop_event):
    while not stop_event.is_set():
        #turn all sensors green
        led_driver.set_all(Color(0, 40, 0))
        sleep(.4)
        led_driver.clear_all()
        if stop_event.is_set():
            break
        sleep(.4)

try:
    while button_pressed != 2:
        combination_force()
        sleep(.5)
    led_driver.clear_all()
    sensor_driver.stop()
    exit()

except KeyboardInterrupt:
    led_driver.clear_all()
    sensor_driver.stop()
    exit()