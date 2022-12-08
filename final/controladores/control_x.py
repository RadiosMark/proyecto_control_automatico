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

num1 = [-(g*m*m)/20,-(g*m*((bu-bv)*np.sin(theta) + bv))/20]
den1 = [20/20, 20200/20, 200500/20, 500000/20, 0 ,0]
sys1 = tf(num1,den1)
k = tf([-15,-3,0.0001],[1,0])
print(k)
sys2 = feedback(sys1,k)

sys3 = series(sys2, tf([-1],[1]))

t_array = np.arange(0,100,0.001)
y, t = step(sys3,t_array)

fig2 = plt.figure()
fig2.canvas.set_window_title('Closed loop step response (Ts=0.001)')
plt.plot(t, y)
plt.xlabel('t [s]')
plt.ylabel('y')
plt.grid()
plt.show()


### revisamos error en régimen permanente
print(sys3)

error = tf([1, 1010, 1.002e+04, 2.574e+04, 3826, 735.8, 0],[1, 1010, 1.002e+04, 2.574e+04, 3826+ 49.05, 735.8+245.2, 0])


