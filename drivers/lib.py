#imports 
from rpi_ws281x import Color
from time import sleep

#function to run the hit color test
def color_change(led_drive, index, value, delay=0.5):
    #if the last value in captured_values is 0, turn the first led red

    if value <.5:
        led_drive.set_ring_color(index, Color(40, 40, 0))
    elif value <.8:
        led_drive.set_ring_color(index, Color(40, 0, 0))
    else:
        led_drive.set_ring_color(index, Color(40, 0, 40))
    sleep(delay)
    led_drive.clear(index)

def await_hit(sensor_drive):
    capture_len = len(sensor_drive.captured_values) #get the length of the captured values
    while True:
        updated_len = len(sensor_drive.captured_values) #get an updated length of the captured values
        if updated_len > capture_len:
            return sensor_drive.captured_values[updated_len-1]['sensor']
        sleep(0.01)

def get_hit(sensor_drive):
    capture_len = len(sensor_drive.captured_values) #get the length of the captured values
    return sensor_drive.captured_values[capture_len-1]['sensor'], sensor_drive.captured_values[capture_len-1]['value'] #return the last value in the captured values