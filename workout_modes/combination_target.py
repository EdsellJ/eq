#Combination Target
'''
Same as specific target training, however, the user can choose multiple target
locations to train on creating customized combinations.
'''
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

def blink_all(stop_event, pause_event, sensor = None, color = Color(0, 40, 0)):
    while not stop_event.is_set():
        if sensor is None:
            #turn all sensors green
            led_driver.set_all(color)
        else:
            #Blink single sensor other color
            led_driver.set_ring_color(sensor, color)    
        sleep(.4)
        if pause_event.is_set():
            pause_event.clear()
            sleep(.5)
        led_driver.clear_all()
        if stop_event.is_set():
            break
        sleep(.4)
        if pause_event.is_set():
            pause_event.clear()
            sleep(.5)

def flash_combination(combination):
    #flash the combination
    for i in combination:
        print("index: ", i)
        led_driver.set_ring_color(i , Color(0, 40, 0))
        sleep(.4)
        led_driver.clear(i)
        sleep(.4)

#function to build the user created combination
def build_combination():
    sensor_driver.start()
    combination = []
    #set last hit to 5 seconds ago
    time_of_last_hit = time.time() - 5
    global button_pressed
    global exit_event
    blink_pause_event = threading.Event()
    if exit_event.is_set():
        exit_event.clear()
    #check that exit event is not set and that there has been no
    blink = threading.Thread(target=blink_all, args=(exit_event, blink_pause_event, None, Color(0, 40, 0)))
    blink.start()
    #hit in the last 50ms
    while not exit_event.is_set() and time.time() - time_of_last_hit > .05:
        #blink all in a thread
        sensor = await_hit(sensor_driver, exit_event)
        if exit_event.is_set():
            break
        if sensor != None:
            blink_pause_event.set()
            combination.append(sensor)
        time_of_last_hit = time.time() #set time of last hit to protect against misinputs
        print(combination)
        sense, color = get_hit(sensor_driver)
        #threading.Thread(target=color_change, args=(led_driver, sense, color)).start()
        color_change(led_driver, sense, color)
    sensor_driver.stop()
    print("leaving build")
    blink.join()
    return combination

def combination_target():
    global button_pressed
    global exit_event
    while not exit_event.is_set() and button_pressed != 2:
        #build combination
        combination = build_combination()
        if exit_event.is_set() and button_pressed == 2:
            return
        else:
            button_pressed = 0
            exit_event.clear()
        
        while not exit_event.is_set():
            #sleep
            sleep(.5)
            #flash the combination
            flash_combination(combination)
            #run user created combination
            sleep(.5) #delay before lighting up current target
            for i in range(len(combination)):
                sensor_driver.start(combination[i])
                led_driver.set_ring_color(combination[i], Color(0, 40, 0))
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
        #rebuild if exit event is set
        if exit_event.is_set():
            #exit if button 2 pressed
            if button_pressed == 2:
                return
            button_pressed = 0
            exit_event.clear()
            continue
        else:
            exit_event.clear()
            button_pressed = 0
            return

try:
    while button_pressed != 2:
        combination_target()

    print("Exiting")
    exit_event.set()
    led_driver.clear_all()
    sensor_driver.stop()
    exit()

except KeyboardInterrupt:
    print("Exiting")
    exit_event.set()
    led_driver.clear_all()
    sensor_driver.stop()
    exit()