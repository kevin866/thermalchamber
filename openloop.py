import serial
import time
import matplotlib.pyplot as plt
import re
kp = 20.0

# Setpoint and Arduino communication parameters
setpoint = float(input("Set your design temperature in Fahrenheit: "))  # Change this value to your desired setpoint
arduino_port = '/dev/tty.usbmodem21101'  # Replace with your Arduino's serial port
baud_rate = 9600

# Initialize the serial connection to the Arduino
arduino = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Wait for Arduino to initialize

numeric_pattern = r"[-+]?\d*\.\d+|\d+"

# Initialize lists to store temperature and time data
time_data = []
temperature_data = []
pwm_data = []
# Set up the real-time plot
plt.ion()  # Turn on interactive mode for real-time plotting
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Temperature')
line2, = ax.plot([], [], label='PWM')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Temperature (Fahrenheit)')
ax.set_title('Real-Time Temperature vs. Time')
ax.grid(True)

# Main PID control loop
try:
    while True:
        # Read the analog value from A1
        arduino.write(b"R\n")
        # analog_value = int(arduino.readline().strip())
        data_bytes = arduino.readline()
        data_str = data_bytes.decode(errors='ignore').strip()

        # Use regular expressions to extract numeric values from the string
        numeric_values = re.findall(numeric_pattern, data_str)
        print(numeric_values)
        numeric_values = float(numeric_values[0])
        temp = float(numeric_values)
        

        # Calculate the error
        error = setpoint - temp

        # Calculate PID terms
        proportional = kp * error

        # Calculate the PWM value
        pwm_value = proportional

        # Ensure PWM value is within limits (0 to 255)
        if pwm_value < 0:
            pwm_value = 0
        elif pwm_value > 255:
            pwm_value = 255
        print(pwm_value)

        # Output the PWM value to pin 7
        arduino.write(f"P{int(pwm_value)}\n".encode())


        # Store the current time and temperature data
        current_time = time.time()
        temperature_data.append(temp)
        time_data.append(current_time)
        pwm_data.append(pwm_value)

        # Update the real-time plot
        line1.set_data(time_data, temperature_data)
        line2.set_data(time_data, pwm_data)
        ax.relim()
        ax.autoscale_view()

        # Pause briefly to control the update rate (adjust as needed)
        plt.pause(0.1)

except KeyboardInterrupt:
    # Close the serial connection when the script is terminated
    arduino.close()

# Turn off interactive mode and display the final plot
plt.ioff()
plt.show()
