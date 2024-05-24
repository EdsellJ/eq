#Speed game
from time import sleep
from signal import pause
import random
import threading
from ringctl import LEDRingDriver
from filmsense import FilmSensor
from rpi_ws281x import Color
# Set up the button, LED, and buzzer
buzz = TonalBuzzer(25)
num_rings = 3
leds_per_ring = 8
led_driver = LEDRingDriver(num_rings, leds_per_ring)

# Set up the potentiometer
pot = MCP3008(channel=7)

#Define array for tones
tones = [Tone("C4"), Tone("D4"), Tone("E4"), Tone("F4")]

#Define arrays for remembering the sequence
sequence = []
user_sequence = []
userStatus = True
list_lock = threading.Lock()
exit_event = threading.Event()

def sequence_match():
    global sequence
    global user_sequence
    return len(user_sequence) == len(sequence) and all(user_sequence[i] == sequence[i] for i in range(len(user_sequence)))

#Function to add a random number to the sequence
def add_to_sequence():
    global sequence
    with list_lock: #ensure only one thread can access the list at a time
        sequence.append(random.randint(0, num_rings-1))
    print("Sequence: ", sequence)

    #blink lights in sequence
    for i in sequence:
        led_driver.set_ring_color(i, Color(0, 40, 0))
        buzz.play(tones[i])
        sleep(0.3)
        led_driver.clear()
        buzz.stop()
        sleep(0.3)

def poll_buttons():
    
    exit_event.wait()  # Wait for the event to be set This will block here waiting for button events

def on_button_press(pressed):
    global user_sequence
    global userStatus
    with list_lock:
        user_sequence.append(pressed)
    tone_thread = threading.Thread(target=play_tone, args=(pressed,))
    tone_thread.daemon = True
    tone_thread.start()
    print("User Sequence: ", user_sequence)
    if sequence_match():
        print("Sequence matched!")
        exit_event.set()
        user_sequence.clear()
    elif len(user_sequence) > len(sequence) or not all(user_sequence[i] == sequence[i] for i in range(len(user_sequence))):
        print("Sequence mismatch. Try again.")
        user_sequence.clear()  # Reset the sequence if wrong
        userStatus = False
        exit_event.set()

def play_tone(tone):
    buzz.play(tones[tone])
    sleep(0.1)
    buzz.stop()

# Simulation function that runs the game
def run_game():
    num_sensors = 3 # Example: 3 sensors connected to channels 0, 1, 2
    handler = FilmSensor(num_sensors)
    handler.start()

    try:
        #play the starting tone
        buzz.play(Tone("C4"))
        sleep(.15)
        buzz.play(Tone("D4"))
        sleep(.15)
        buzz.play(Tone("E4"))
        sleep(.15)
        buzz.play(Tone("F4"))
        sleep(.4)
        buzz.stop()
        sleep(1)
        while userStatus:
            add_to_sequence()

            exit_event.clear()

            sleep(1)

        #play the losing tone
        buzz.play(Tone("G4"))
        sleep(.2)
        buzz.play(Tone("F4"))
        sleep(.2)
        buzz.play(Tone("E4"))
        sleep(.4)
        buzz.stop()

    except KeyboardInterrupt:
        led_driver.clear()
        handler.stop()
        buzz.stop()

# Run the game
run_game()
