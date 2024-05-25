#Combination Speed
'''
The Equalizer illuminates a sequence of LED target locations Green. The user is
then required to accurately repeat the sequence. As the user succeeds, one
additional target location is added to the sequence, thus the sequence becomes
longer and more complex. Once the user fails to repeat the sequence, or the time
expires, the training is over. The LED target location will illuminate Green, once
the user has struck the target, the LED will no longer illuminate. When the
sequence restarts, the LED will again illuminate Green.
'''
from common_imports import *
import common_imports
led_driver, sensor_driver = common_imports.setup_drivers()
from drivers.lib import color_change, get_hit, await_hit
# Arrays for sequence
#Define arrays for remembering the sequence
sequence = []
user_sequence = []
# Threading variables
userStatus = True
list_lock = threading.Lock()
exit_event = threading.Event()

# Function to check if the user sequence matches the sequence
def sequence_match():
    global sequence
    global user_sequence
    global userStatus
    user_sequence = [item['sensor'] for item in sensor_driver.captured_values]
    
    print(user_sequence)
    #if not a perfect match, check for match up to current length of user sequence
    if len(user_sequence) == len(sequence) and all(user_sequence[i] == sequence[i] for i in range(len(user_sequence))):
        return True
    elif len(user_sequence) > len(sequence) or not all (user_sequence[i] == sequence[i] for i in range(len(user_sequence))):
        print("sequence mismatch. try again.")
        sensor_driver.captured_values.clear() #reset user sequence if wrong
        userStatus = False
        return False
    else:
        return False

#Function to add a random number to the sequence
def add_to_sequence():
    global sequence
    with list_lock: #ensure only one thread can access the list at a time
        sequence.append(random.randint(0, led_driver.num_rings-1))
    print("Sequence: ", sequence)

    #blink lights in sequence
    for i in sequence:
        led_driver.set_ring_color(i, Color(0, 40, 0))
        sleep(0.3)
        led_driver.clear(i)
        sleep(0.3)

def run_game():
    sensor_driver.start()

    try:
        while True:
            if not userStatus:
                break
            add_to_sequence()
            user_sequence.clear()
            while not sequence_match() and userStatus:
                await_hit(sensor_driver)
                sensor, value = get_hit(sensor_driver)
                #change the color of the sensor in a thread
                with threading.Lock():
                    threading.Thread(target=color_change, args=(led_driver, sensor, value)).start()

            sensor_driver.captured_values.clear()
            sleep(1)
    except KeyboardInterrupt:
        sensor_driver.stop()
        led_driver.clear_all()
        exit()

# Start the game
run_game()
sensor_driver.stop()
led_driver.clear_all()
exit()