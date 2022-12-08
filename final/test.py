from numpy import *
from control import *
########################### variables

l = 0.5
m = 10
I = 0.1
bu = 50
bv = 50
bw = 100
g = 9.81

### cond iniciales

theta = pi/2


num8 = [1/l]
den8 = [1, bw/l,0]

theta = tf(num8, den8)
print(theta)

thetass = ss(theta)
print(thetass)

A = [[-200.  , -0.],
     [   1. ,   0.]]
B = [[1.],
     [0.]]
C = ctrb(A, B)
print(C)

O = obsv(A,C)
print(linalg.det(C))
print(linalg.det(O))