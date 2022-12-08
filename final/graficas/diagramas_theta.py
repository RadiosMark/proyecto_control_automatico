from numpy import *
from control.matlab import *
import matplotlib.pyplot as plt

l = 0.5
m = 10
I = 0.1
bu = 50
bv = 50
bw = 100
g = 9.81
theta = pi/2

# LGR para theta

num1 = [1]
den1 = [I, bw, 0]
sys1 = tf(num1,den1)

r,k = rlocus(sys1)
plt.title('LGR Theta')
fig0 = plt.gcf()
fig0.canvas.set_window_title('LGR Theta')
plt.grid()
#plt.show()

# Bode para theta
fig1 = plt.figure()
fig1.canvas.set_window_title("Diagrama de Bode Theta")
bode(sys1, logspace(-1,6,500), dB = True, Hz=False)

#plt.show()
fig2 = plt.figure()
fig2.canvas.set_window_title('Diagrama de Nyquist de Theta')
nyquist(sys1,logspace(-1,6,500),labelFreq=10)
#nyquist(sys1,omega=[0.01,100],labelFreq=10)
plt.grid()
#plt.show()