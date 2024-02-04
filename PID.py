import serial
import time

# Define PID parameters
kp = 1.0  # Proportional gain
ki = 0.1  # Integral gain
kd = 0.2  # Derivative gain

# Initialize PID variables
previous_error = 0
integral = 0

# Setpoint and Arduino communication parameters
setpoint = input("Set your design temperature in Fahrenheit: ")  # Change this value to your desired setpoint
arduino_port = '/dev/tty.usbmodem21101'  # Replace with your Arduino's serial port
baud_rate = 9600

# Initialize the serial connection to the Arduino
arduino = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Wait for Arduino to initialize

# Main PID control loop
try:
    while True:
        # Read the analog value from A1
        arduino.write(b"R\n")
        analog_value = int(arduino.readline().strip())

        # Calculate the error
        error = setpoint - analog_value

        # Calculate PID terms
        proportional = kp * error
        integral += ki * error
        derivative = kd * (error - previous_error)

        # Calculate the PWM value
        pwm_value = proportional + integral + derivative

        # Ensure PWM value is within limits (0 to 255)
        if pwm_value < 0:
            pwm_value = 0
        elif pwm_value > 255:
            pwm_value = 255

        # Output the PWM value to pin 7
        arduino.write(f"P{int(pwm_value)}\n")

        # Store the current error for the next iteration
        previous_error = error

        # Delay for a short period (adjust as needed)
        time.sleep(0.1)

except KeyboardInterrupt:
    # Close the serial connection when the script is terminated
    arduino.close()
