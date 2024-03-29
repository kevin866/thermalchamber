import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Establish serial connection to Arduino
# Replace 'COM3' with your Arduino's serial port
ser = serial.Serial('/dev/tty.usbmodem21101', 9600, timeout=1)
time.sleep(2) # Wait for the connection to establish

# Lists to store temperature data
times = []
desired_temps = []
recorded_temps = []
def temperature_to_volt(desired_temp):
    # Simplified function to convert temperature to PWM value
    pwm = float(desired_temp-32)/1.8/100
    print("corresponding pwm value for the desired tempeature:", pwm)
    return pwm
# Ask for desired temperature
desired_temp_f = float(input("Enter the desired temperature in Fahrenheit: "))
pwm_value = temperature_to_volt(desired_temp_f)



def update_plot(frame):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        recorded_temp = float(line)/100.0 # Simulated as direct temperature for simplicity
        
        print("Analog value (simulated temperature):", recorded_temp)
        
        # Append data for plotting
        times.append(time.time())
        desired_temps.append(pwm_value)
        recorded_temps.append(recorded_temp)
        
        # Update plot
        plt.cla() # Clear the current axes
        plt.plot(times, desired_temps, label="Desired Temperature in volts")
        plt.plot(times, recorded_temps, label="Recorded Temperature in volts")
        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Temperature (F)')
        plt.tight_layout()
        
        # Send PWM value to Arduino
        print("Sending PWM value:", pwm_value)
        # ser.write(str(pwm_value).encode())

# Setting up plot
plt.figure()
ani = FuncAnimation(plt.gcf(), update_plot, interval=1000)

plt.tight_layout()
plt.show()
