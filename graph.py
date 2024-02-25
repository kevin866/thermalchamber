import numpy as np
import serial
import time
import matplotlib.pyplot as plt
#
# Load the array from the file
T1 = np.load('T1.npy')+2.5
T2 = np.load('T2.npy')
T3 = np.load('T3.npy')
recorded_temps = np.load('Temp.npy')
times = np.load('times.npy')

plt.plot(times, recorded_temps, label="Recorded Temperature (C)")
plt.plot(times, T1, label="T1 Temperature (29.5 C) ")
plt.plot(times, T2, label="T2 Temperature (32 C)")
plt.plot(times, T3, label="T3 Temperature (46 C)")
plt.legend()
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.tight_layout()
plt.show()