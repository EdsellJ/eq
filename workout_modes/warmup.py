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
from drivers.lib import color_change, await_hit, get_hit

#function to light random sensor
def light_random():
    #generate random number
    rand_num = random.randint(0, led_driver.num_rings-1)
    #turn sensor green
    led_driver.set_ring_color(rand_num, Color(0, 40, 0))
    return rand_num


def warmup():
    sensor_driver.start()
    start_time = time.time()
    while time.time() - start_time < 60:
        rand = light_random()
        while True:
            hit = await_hit(sensor_driver)
            sensor, value = get_hit(sensor_driver)
            #change the color of the sensor in a thread
            with threading.Lock():
                threading.Thread(target=color_change, args=(led_driver, sensor, value)).start()
            color_change(led_driver, sensor, value)
            sleep(0.1)
            if hit == rand:
                break
    
    print("Warmup Complete")
    sleep(1)
    

try:
    warmup()
    sensor_driver.stop()
    led_driver.clear_all()

except KeyboardInterrupt:
    sensor_driver.stop()
    led_driver.clear_all()
    exit()