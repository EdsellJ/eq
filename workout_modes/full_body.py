#Full Body 
'''
All target locations are illuminated Green at the same time. The goal is for the
user to turn all LED sensors Red as quickly as possible. This is a timed event.
'''
from common_imports import *
import common_imports
from color_change import color_change
led_driver, sensor_driver = common_imports.setup_drivers()

#create an array of 0..the number of sensors

#function to light all sensors green
def light_all():
    #turn all sensors green
    for i in range(led_driver.num_rings):
        led_driver.set_ring_color(i, Color(0, 40, 0))

#function to find what sensors have been hit
def find_if_all_hit():
    #fill test array with values 0 to number of sensors
    test_arr = sensor_driver.channels

    #check sensors for hits
    capture_len = len(sensor_driver.captured_values)
    if capture_len > 0:
        for i in range(capture_len):
            #if the sensor is in the test array, remove it
            if sensor_driver.captured_values[i]['sensor'] in test_arr: 
                test_arr.remove(sensor_driver.captured_values[i]['sensor'])
                #clear led in the sensor index
                led_driver.clear(sensor_driver.captured_values[i]['sensor'])
                sleep(.1)
                #change the color of the sensor in a thread
                with threading.Lock():
                    threading.Thread(target=color_change, args=(led_driver, sensor_driver.captured_values[i]['sensor'], sensor_driver.captured_values[i]['value'])).start()

    print(test_arr)
    #if test_arr is empty return false
    if not test_arr:
        return False
    else:
        return True
    
def full_body():
    light_all()
    sensor_driver.start()
    while find_if_all_hit():
        sleep(0.1)

try:
    full_body()
    sleep(1)
    sensor_driver.stop()
    led_driver.clear_all()
    exit()

except KeyboardInterrupt:
    sensor_driver.stop()
    led_driver.clear_all()
    exit()