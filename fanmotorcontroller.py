import serial
import matplotlib.pyplot as plt
from drawnow import drawnow
import time
import numpy as np
# Initialize lists to store data
desired_data = []
current_data = []

# Create serial connection (adjust port and baudrate accordingly)
ser = serial.Serial('COMX', 9600)

# Function to update plot
def update_plot():
    plt.plot(desired_data, label='Desired Value')
    plt.plot(current_data, label='Current Value')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Desired vs Current Value over Time')
    plt.legend()
    plt.grid(True)

# Main loop to read data and plot
while True:
    try:
        # Read data from Arduino
        data = ser.readline().decode().strip().split(' ')
        if len(data) == 3:  # Ensure valid data format
            current_data.append(float(data[1]))
            desired_data.append(float(data[3]))

            # Update plot
            drawnow(update_plot)
            plt.pause(0.000001)

    except KeyboardInterrupt:
        print("Program Interrupted")
        break
np.save('current angle.npy', current_data)
np.save('setpoints.npy', desired_data)

# Close serial connection
ser.close()
