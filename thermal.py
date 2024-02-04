import serial
import time
import matplotlib.pyplot as plt
import re  # Import the regular expressions library
import scipy.io as sio
# Set the serial port name and baud rate (must match Arduino settings)
port = '/dev/tty.usbmodem21101'  # Change to the appropriate port on your computer
baud_rate = 9600  # Must match the baud rate set in your Arduino sketch
ser = serial.Serial(port, baud_rate)
# Open the serial port
print(f"Connected to {port} at {baud_rate} baud")
# Initialize empty lists to store data
time_data = []
sensor_data = []
# Regular expression pattern to extract numeric values (including decimal point)
numeric_pattern = r"[-+]?\d*\.\d+|\d+"
# Define PID parameters
kp = 1.0  # Proportional gain
ki = 0.1  # Integral gain
kd = 0.2  # Derivative gain

# Initialize PID variables
previous_error = 0
integral = 0

# Setpoint and Arduino communication parameters
setpoint = input("Set your design temperature in Fahrenheit: ")  # Change this value to your desired setpoint
time.sleep(2)  # Wait for Arduino to initialize
try:
    # Record data for 2 minutes
    end_time = time.time() + 120  # 2 minutes (120 seconds)
    while time.time() < end_time:
        # Read data from the serial port as bytes
        data_bytes = ser.readline()
        current_time = time.time()
        
        # Convert bytes to string
        data_str = data_bytes.decode(errors='ignore').strip()
        
        # Use regular expressions to extract numeric values from the string
        numeric_values = re.findall(numeric_pattern, data_str)
        
        if numeric_values:
            # Assuming there may be multiple numeric values in a single line,
            # we'll take the first one (index 0) as the sensor data.
            numeric_values = float(numeric_values[0])
            sensor_value = float(numeric_values)
            print(sensor_value)
            # print(sensor_data,end='\n')
            if 33.0<sensor_value<200.0:
                time_data.append(current_time)
                sensor_data.append(sensor_value)
        
        
    # Close the serial port when done
    ser.close()
    print(sensor_data)
    sio.savemat('temp.mat', {'my_array': sensor_data})
    # Plot the data
    plt.plot(time_data, sensor_data)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Sensor Data')
    plt.title('Sensor Data vs. Time')
    plt.grid(True)
    plt.show()

except serial.SerialException:
    print(f"Failed to connect to {port}")
except KeyboardInterrupt:
    print("Exiting program")
finally:
    ser.close()  # Ensure the serial port is closed if an exception occurs