from gpiozero import MCP3208
import time
import threading
class FilmSensor:

    def __init__(self, num_sensors):
        self.num_sensors = num_sensors
        self.channels = list(range(num_sensors))
        self.sensors = [MCP3208(channel=channel) for channel in self.channels]
        self.time_limit = 0.18
        self.threshold = 0.06
        self.when_triggered = None
        self.threads = []
        self.captured_values = []  # List to store captured values
        self.lock = threading.Lock()  # Lock to prevent multiple threads from accessing the list simultaneously

        #for capture
        self.consecutive_decreases_allowed = 3

        self.shutdown_event = threading.Event()  # Event to signal shutdown

        

    def capture (self, channel, initial_value):
        sensor = self.sensors[channel]
        largest_value = initial_value
        time_limit = self.time_limit
        value_threshold = self.threshold
        consecutive_decreases_allowed = self.consecutive_decreases_allowed # Allowable consecutive decreases before terminating early

        value = sensor.value
        # If larger than threshold, capture current time to then capture the largest value within 180ms after initial hit
        start_time = time.time()  # Start of 180ms
        previous_value = value  # Initialize previous value
        consecutive_decreases = 0  # Reset consecutive decrease count

        while time.time() - start_time < time_limit:
            value = sensor.value
            if value > largest_value:
                largest_value = value
                consecutive_decreases = 0  # Reset decreases count on new peak
            elif value < previous_value:
                consecutive_decreases += 1  # Increment decreases count
                if consecutive_decreases >= consecutive_decreases_allowed:
                    break  # Early exit if value has peaked and started decreasing
            else:
                consecutive_decreases = 0  # Reset if value does not decrease

            previous_value = value  # Update previous value for next iteration

        with self.lock: #lock to make accesssing the list thread safe
            self.captured_values.append({'sensor': channel, 'value': largest_value})  # Append the largest value to the list

        #print capture_values to console with formatting
        captured_values_str = ', '.join([f"{item['sensor']}: {item['value']:.2f}" for item in self.captured_values])
        print(f"Captured values: {captured_values_str}")


                
        return largest_value

    def start(self):
        for i, sensor in enumerate(self.sensors):
            thread = threading.Thread(target=self._monitor_sensor, args=(sensor, i))
            thread.start()
            self.threads.append(thread)
        self.shutdown_event.clear()  # Clear the shutdown event
    
    def stop(self):
        self.shutdown_event.set()  # Signal all threads to shutdown
        for thread in self.threads:
            thread.join()

    def _monitor_sensor(self, sensor, index):
        print(f"Monitoring force sensor on channel {sensor.channel}...")
        while not self.shutdown_event.is_set():
            value = sensor.value
            if value > self.threshold:
                self.capture(index, value)  # Call capture directly                # Wait until the value drops below the threshold to reset
                while not self.shutdown_event.is_set() and sensor.value > self.threshold:
                    time.sleep(0.02)
            time.sleep(0.01) #small delay to reduce cpu usage

def on_force_detected(channel, value):
    print(f"Force detected on channel {channel} with value: {value}")

# Example usage
if __name__ == "__main__":
    num_sensors = 8 # Example: 3 sensors connected to channels 0, 1, 2
    handler = FilmSensor(num_sensors)
    handler.start()

    try:
        # Keep the main program running while sensors are monitored
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping sensors...")
        handler.stop()