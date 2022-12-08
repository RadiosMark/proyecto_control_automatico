import numpy as np
from control.matlab import *
import matplotlib.pyplot as plt

l = 0.5
m = 10
I = 0.1
bu = 50
bv = 50
bw = 100
g = 9.81
theta = np.pi/2

num1 = [np.sin(theta)/m]
den1 = [1,bu/m,0]
sys1 = tf(num1,den1)
k = tf([10,100,0],[1,0])
print(k)
sys2 = feedback(sys1,k)

t_array = np.arange(0,20,0.001)
y, t = step(sys2,t_array)

fig2 = plt.figure()
fig2.canvas.set_window_title('Closed loop step response (Ts=0.001)')
plt.plot(t, y)
plt.xlabel('t [s]')
plt.ylabel('y')
plt.grid()
plt.show()