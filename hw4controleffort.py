import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Establish serial connection to Arduino
ser = serial.Serial('/dev/tty.usbmodem21101', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

# Lists to store data
times = []
desired_temps = []
recorded_temps = []
control_efforts = []  # New list for control efforts

def temperature_to_volt(desired_temp):
    # Function to convert temperature to PWM value (simplified)
    pwm = float(desired_temp - 32) / 1.8 / 100
    print("Corresponding PWM value for the desired temperature:", pwm)
    return pwm

# Ask for desired temperature
desired_temp_f = float(input("Enter the desired temperature in Fahrenheit: "))
pwm_value = temperature_to_volt(desired_temp_f)

def update_plot(frame):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        parts = line.split(',')  # Assuming data is sent as 'temperature,controlEffort'
        if len(parts) == 2:
            recorded_temp, control_effort = float(parts[0]) / 100.0, float(parts[1])/1000.0
            print("Recorded temperature:", recorded_temp, "Control Effort:", control_effort)
            
            # Append data for plotting
            current_time = time.time()
            times.append(current_time)
            desired_temps.append(pwm_value)
            recorded_temps.append(recorded_temp)
            control_efforts.append(control_effort)  # Append control effort
            
            # Update plot
            plt.cla()
            plt.plot(times, desired_temps, label="Desired Temperature (V)")
            plt.plot(times, recorded_temps, label="Recorded Temperature (V)")
            plt.plot(times, control_efforts, label="Control Effort (A0 Reading) scaled down by 10", linestyle='--')  # Plot control effort
            plt.legend()
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.tight_layout()
        
            # Optionally, send PWM value to Arduino
            # ser.write(str(pwm_value).encode())

# Setting up plot
plt.figure()
ani = FuncAnimation(plt.gcf(), update_plot, interval=1000)

plt.tight_layout()
plt.show()
