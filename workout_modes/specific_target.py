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
from queue import Queue
led_driver, sensor_driver = common_imports.setup_drivers()
from gpiozero import Button, TonalBuzzer
from gpiozero.tones import Tone
from drivers.lib import color_change, await_hit, get_hit

#define button 1, 2 and buzzer
button1 = Button(5)
button2 = Button(13)
buzz = TonalBuzzer(24)

#function to beep buzzer for 1 second
def beep(duration = .075):
    buzz.play(Tone("D5"))
    sleep(duration)
    buzz.stop()

def positive_tune():
    buzz.play(Tone("D5"))
    sleep(.125)
    buzz.stop()
    buzz.play(Tone("E5"))
    sleep(.125)
    buzz.play(Tone("F5"))
    sleep(.125)
    buzz.play(Tone("G5"))
    sleep(.25)
    buzz.stop()
    
def negative_tune():
    buzz.play(Tone("G5"))
    sleep(.125)
    buzz.stop()
    buzz.play(Tone("F5"))
    sleep(.125)
    buzz.play(Tone("E5"))
    sleep(.125)
    buzz.play(Tone("D5"))
    sleep(.25)
    buzz.stop()

def blink_all(stop_event, sensor = None, color = Color(0, 40, 0)):
    while not stop_event.is_set():
        if sensor is None:
            #turn all sensors green
            led_driver.set_all(color)
        else:
            #Blink single sensor other color
            led_driver.set_ring_color(sensor, color)    
        sleep(.4)
        led_driver.clear_all()
        if stop_event.is_set():
            break
        sleep(.4)

def flash_green(sensor, origional_color):
    led_driver.set_ring_color(sensor, Color(0, 40, 0))
    sleep(.4)
    led_driver.set_ring_color(sensor, origional_color)

def color_picker(color_stop_event, sensor, color_queue):
    #cycle through colors
    colors = [Color(40, 40, 0), Color(40, 0, 0), Color(40, 0, 40)]
    color = colors[0]
    while not color_stop_event.is_set():
        blink_stop_event = threading.Event()
        #start a thread of blink all that I can join later
        with threading.Lock():
            thread = threading.Thread(target=blink_all, args=(blink_stop_event, sensor, color))
            #start the thread as a daemon
            thread.daemon = True
            thread.start()
        #wait for button 2 to be pressed
        while not button2.is_pressed and not color_stop_event.is_set():
            sleep(0.01)
        #beep on button press in a thread
        threading.Thread(target=beep).start()
        blink_stop_event.set()
        thread.join()
        #if exit set
        if color_stop_event.is_set():
            break
        #if on last color, reset
        if color == colors[-1]:
            color = colors[0]
        else:
            color = colors[colors.index(color)+1]
        
    color_queue.put(color)  # Put the color into the queue


def getColor(sensor):
    color_queue = Queue()
    color_stop_event = threading.Event()
    color_thread = threading.Thread(target=color_picker, args=(color_stop_event, sensor, color_queue))
    color_thread.daemon = True
    color_thread.start()
    while await_hit(sensor_driver) != sensor:
        sleep(0.02)
    color_stop_event.set()
    color_thread.join()
    return color_queue.get()  # Get the color from the queue

def startup():
    stop_event = threading.Event()
    #start a thread of blink all that I can join later
    with threading.Lock():
        thread = threading.Thread(target=blink_all, args=(stop_event,))
        #start the thread as a daemon
        thread.daemon = True
        thread.start()
    
    #wait for the user to hit a sensor
    training_sensor = await_hit(sensor_driver)
    #beep in a thread
    threading.Thread(target=beep).start()
    #signal the blink all thread to stop
    stop_event.set()
    #wait for the blink all thread to finish
    thread.join()
    return training_sensor

def training_loop(training_exit_event, sensor, color):
    #start the sensor driver
    sensor_driver.start(sensor)
    #set the color of the training sensor
    led_driver.set_ring_color(sensor, color)
    #determine force threshold for color
    if color == Color(40, 40, 0):
        force_threshold = 0.2
    elif color == Color(40, 0, 0):
        force_threshold = 0.4
    else:
        force_threshold = 0.5
    #wait for the sensor to be hit
    while not training_exit_event.is_set():
        await_hit(sensor_driver, training_exit_event)
        if training_exit_event.is_set():
            break
        #check if force matches correct threshold for color
        sense, force = get_hit(sensor_driver)
        if force >= force_threshold:
            #play positive tune in a thread
            threading.Thread(target=positive_tune).start()
            #flash green in a thread
            threading.Thread(target=flash_green, args=(sensor, color)).start()
        else:
            #play negative tune in a thread
            threading.Thread(target=negative_tune).start()
        sleep(0.02)

def specific_target():
    #beep
    beep()
    #set the training sensor to the sensor that was hit
    training_sensor = startup()
    color = getColor(training_sensor) # Get the color for the training sensor
    #set the color of the training sensor
    sensor_driver.stop()
    #wait for all threads to stop
    sleep(0.5)
    exit_event = threading.Event()
    #start training loop in a thread
    thread = threading.Thread(target=training_loop, args=(exit_event, training_sensor, color))
    thread.daemon = True
    thread.start()
    #if button 1 is pressed stop the training loop
    while not button1.is_pressed:
        sleep(0.02)
    exit_event.set()
    thread.join()    
    led_driver.clear_all()
    sensor_driver.stop()
    sleep(.3) #wait for sensor driver to stop

try:
    while True:
        sensor_driver.start()
        specific_target()
        led_driver.clear_all()

except KeyboardInterrupt:
    sensor_driver.stop()
    led_driver.clear_all()
    exit()


