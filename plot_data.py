import numpy as np
import matplotlib.pyplot as plt
import scipy.io
# Step 1: Import necessary libraries

# Step 2: Read the .npy data file
cur_angle = np.load('current angle.npy')
setpoints = np.load('setpoints.npy')
scipy.io.savemat('cur_angle.mat', {'cur_angle': cur_angle})
scipy.io.savemat('setpoints.mat', {'setpoints': setpoints})

time = np.linspace(0,450,450)/100
print(time.shape)
scipy.io.savemat('time.mat', {'time': time})

# Step 3: Plot the data
plt.plot(time, cur_angle[0:450], label='Current Angle')
plt.plot(time, setpoints[0:450], label='Desired Angle')
# plt.plot(times, desired_data, label='Desired Angle')
# plt.plot(times, current_data, label='Current Angle')
plt.xlabel('Time (s)')
plt.ylabel('Angle (degrees)')
plt.title('Desired vs Current Angle over Time')
plt.legend()
plt.show()
