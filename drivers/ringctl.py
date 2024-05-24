import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color
import time

# Create a class to initialize the LED Rings
class LEDRingDriver:
    #Init fuction to initialize the LED Ring
    def __init__(self, num_rings, leds_per_ring):
        # LED Ring configuration
        self.num_rings = num_rings
        self.leds_per_ring = leds_per_ring

        # LED strip configuration
        self.LED_COUNT = num_rings*leds_per_ring       # Number of LED pixels
        self.LED_PIN = 18             # GPIO pin connected to the pixels (18 uses PWM)
        # self.LED_PIN = 10           # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0)
        self.LED_FREQ_HZ = 800000     # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA = 10             # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT = False       # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL = 0          # Set to '1' for GPIOs 13, 19, 41, 45 or 53

        # Create the PixelStrip object with the above configuration
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ,
                                self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Initialize the library (must be called once before other functions)
        self.strip.begin()

        # Dynamic ring dictionary to map ring indices to their start pixel index
        self.rings = {i: i * leds_per_ring for i in range(num_rings)}

    def set_ring_color(self, ring_index, color):
        """Set the color of all LEDs in a specific ring"""
        start_index = self.rings[ring_index]
        for i in range(self.leds_per_ring):
            self.strip.setPixelColor(start_index + i, color)
        self.strip.show()

    def clear(self):
        """Clear all LEDs"""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

    def set_all(self, color):
        """Set the color of all LEDs"""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

# Example usage:
if __name__ == "__main__":
    num_rings = 4
    leds_per_ring = 8
    led_driver = LEDRingDriver(num_rings, leds_per_ring)
    try:
        # Set all LEDs in the second ring to green
        led_driver.set_ring_color(1, Color(0, 255, 0))
        time.sleep(1)
        # Clear all LEDs
        led_driver.clear()
    except KeyboardInterrupt:
        led_driver.clear()