import serial
import matplotlib.pyplot as plt
from drawnow import drawnow
import numpy as np

# Initialize serial connection
arduino_port = '/dev/tty.usbmodem21101'  # Change this to your Arduino port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

# Initialize plot
plt.ion()
plt.title('Real-time Analog Reading from Arduino')
plt.xlabel('Time')
plt.ylabel('Analog Value')
data = []

# Function to update plot
def update_plot():
    plt.plot(data, 'r-')
    plt.pause(0.1)

# Main loop to read data from Arduino and plot it
try:
    while True:
        # Read data from Arduino
        line = ser.readline().decode('utf-8').strip()
        if line:  # Check if the line is not empty
            analog_value = float(line)
            data.append(analog_value)
        
            # Update plot
            drawnow(update_plot)
except KeyboardInterrupt:
    # Close serial connection
    ser.close()
