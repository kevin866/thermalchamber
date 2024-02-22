import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Establish serial connection to Arduino
ser = serial.Serial('/dev/tty.usbmodem21101', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to establish

# Lists to store data
times = []
T1 = []
T2 = []
T3 = []
recorded_temps = []

def temperature_to_volt(desired_temp):
    # Function to convert temperature to PWM value (simplified)
    pwm = float(desired_temp - 32) / 1.8 / 100
    print("Corresponding PWM value for the desired temperature:", pwm)
    return pwm

# Ask for desired temperature
T11 = float(input("Enter the T1 temperature in Celius: "))
T21 = float(input("Enter the T2 temperature in Celius: "))
T31 = float(input("Enter the T3 temperature in Celius: "))

def update_plot(frame):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        recorded_temp = float(line[0])
        print("Recorded temperature:", recorded_temp)
        
        # Append data for plotting
        current_time = time.time()
        times.append(current_time)
        # desired_temps.append(pwm_value)
        recorded_temps.append(recorded_temp)
        T1.append(T11)
        T2.append(T21)
        T3.append(T31)
        
        # Update plot
        plt.cla()
        plt.plot(times, recorded_temps, label="Recorded Temperature (C)")
        plt.plot(times, T1, label="T1 Temperature (C)")
        plt.plot(times, T2, label="T2 Temperature (C)")
        plt.plot(times, T3, label="T3 Temperature (C)")
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
