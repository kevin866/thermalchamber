import numpy as np
import serial
import time
import matplotlib.pyplot as plt
#
# Load the array from the file
T1 = np.load('T11.npy')
T2 = np.load('T21.npy')
T3 = np.load('T31.npy')
recorded_temps = np.load('Temp1.npy')
times = np.load('times1.npy')

plt.plot(times, recorded_temps, label="Recorded Temperature (C)")
plt.plot(times, T1, label="T1 Temperature (29.5 C) ")
plt.plot(times, T2, label="T2 Temperature (32 C)")
plt.plot(times, T3, label="T3 Temperature (46 C)")
plt.legend()
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.tight_layout()
plt.show()