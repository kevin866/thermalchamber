from pyfirmata import Arduino, util
import time

# Define the Arduino board serial port
board = Arduino('/dev/tty.usbmodem21101')  # Replace with the appropriate port (e.g., COM3 for Windows)

# Set up iterator to avoid buffer overflow
it = util.Iterator(board)
it.start()

# Define the PWM pin (e.g., pin 9)
pwm_pin = board.get_pin('d:9:p')

# Function to set PWM value
def set_pwm_value(pin, value):
    pin.write(value)

# Example: Fade LED on pin 9
try:
    while True:
        set_pwm_value(pwm_pin, 100.0)
except KeyboardInterrupt:
    board.exit()  # Clean up when the program is interrupted
