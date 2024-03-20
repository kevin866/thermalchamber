import serial
import matplotlib.pyplot as plt
from drawnow import drawnow
import time
import numpy as np




# Initialize lists to store data
desired_data = []
current_data = []
times = []

# Create serial connection (adjust port and baudrate accordingly)
ser = serial.Serial('/dev/tty.usbmodem21101', 9600, timeout=1)

# Function to send setpoint to Arduino
def send_setpoint(setpoint):
    ser.write(str(setpoint).encode())
    ser.write(b'\n')

# Prompt user to input setpoint
setpoint = float(input("Enter setpoint angle in degrees: "))
send_setpoint(setpoint)

# Function to update plot
def update_plot():
    plt.plot(times, desired_data, label='Desired Angle')
    plt.plot(times, current_data, label='Current Angle')
    plt.xlabel('Time')
    plt.ylabel('Angle')
    plt.title('Desired vs Current Angle over Time')
    plt.legend()
    plt.grid(True)

# Main loop to read data and plot
while True:
    try:
        # Read data from Arduino
        # data = ser.readline().decode().strip().split(' ')
        line = ser.readline().decode('utf-8').rstrip()
        parts = line.split(',')  # Assuming data is sent as 'temperature,controlEffort'
        if len(parts) == 2:  # Ensure valid data format
            current_data.append(float(parts[0]))
            desired_data.append(float(parts[1]))
            # Append data for plotting
            current_time = time.time()
            times.append(current_time)

            # Update plot
            drawnow(update_plot)
            # plt.pause(0.000001)

    except KeyboardInterrupt:
        print("Program Interrupted")
        break
np.save('current angle.npy', current_data)
np.save('setpoints.npy', desired_data)

# Close serial connection
ser.close()
