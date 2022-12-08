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

################ controlabilidad y observabilidad

# U(s) considerando solo U1(s)
num = [1/m]
den = [1, bu/m]

U = tf(num, den)
print(U)
Uss = ss(U)
print(Uss)
A = [[-5.]] 
B = [[1.]]
C = ctrb(A, B)
print(linalg.det(C)) # controlable
O = obsv(A,C)

print(linalg.det(O)) # observable



# U(s) considerando solo U2(s)

num1 = [-g*m*cos(theta)]
den1 = [1, (bw*m+l*bu)/(m*l), (bw*bu)/(m*l)]

U1 = tf(num1, den1)
print(U1)

Uss1 = ss(U1) 
A = [[ -205., -1000.],[    1.  ,   0.]]
B = [[1.],
     [0.]]
C = ctrb(A, B)
O = obsv(A, C) 

print(O)  

# sistema controlable pero no observable


#----------------------------------------------------------------------------------------------------------------------

# V(s) solo tiene una entrada U2(s)

num2 = [g*m*sin(theta)]
den2 = [1, (bw*m+l*bu)/(m*l), (bw*bu)/(m*l)]

V = tf(num2, den2)
print(V)
Vss = ss(V)
print(Vss)

A = [[ -205., -1000.],[    1.  ,   0.]]
B = [[1.],
     [0.]]
C = ctrb(A, B)

O = obsv(A,C)
print(O) 

# controlable y no observable

#----------------------------------------------------------------------------------------------------------------------

# W(s) solo tiene una entrada U2(s)

num3 = [1/l]
den3 = [1,bw/l]

W = tf(num3, den3)
print(W)

Wss = ss(W)
print(Wss)

A = [[-200.]]
B = [[1.]]
C = ctrb(A, B)

O = obsv(A,C)
print(linalg.det(O)) #observable

# controlable y observable

#----------------------------------------------------------------------------------------------------------------------

#### X(s) depende de 2 entradas 

# considerando solo U1

num4 = [cos(theta)/m]
den4 = [1,bu/m,0]

X = tf(num4, den4)
print(X)

Xss = ss(X)
print(Xss)

A = [[-5. ,-0.],
     [ 1. , 0.]]
B = [[1.],
     [0.]]
C = ctrb(A, B) # controlable 
O = obsv(A,C)
print(linalg(O)) # no observable

# controlable pero no observable

##### sonsiderando solo U2

num5 = [-(g*m*m)/20,-(g*m*((bu-bv)*sin(theta) + bv))/20]
den5 = [20/20, 20200/20, 200500/20, 500000/20, 0 ,0]

X1 = tf(num5, den5)
print(X1)

X1ss = ss(X1)

print(X1ss)
A = [[-1.0100e+03 ,-1.0025e+04 ,-2.5000e+04 ,-0.0000e+00 ,-0.0000e+00],
     [ 1.0000e+00 , 0.0000e+00 , 0.0000e+00 , 0.0000e+00 , 0.0000e+00],
     [ 0.0000e+00 , 1.0000e+00 , 0.0000e+00 , 0.0000e+00 , 0.0000e+00],
     [ 0.0000e+00 , 0.0000e+00 , 1.0000e+00 , 0.0000e+00 , 0.0000e+00],
     [ 0.0000e+00 , 0.0000e+00 , 0.0000e+00 , 1.0000e+00 , 0.0000e+00]]

B = [[1.],
     [0.],
     [0.],
     [0.],
     [0.]]

C = ctrb(A, B)
O = obsv(A, C)
print(linalg.det(O))  ### no observable

## controlable pero no observable
#----------------------------------------------------------------------------------------------------------------------

#### Y(s) depende de 2 entradas 

# considerando solo U1

num6 = [sin(theta)/m]
den6 = [1,bu/m,0]

Y = tf(num6, den6)
print(Y)

Yss = ss(Y)
print(Yss)

A = [[-5. ,-0.],
     [ 1. , 0.]]
B = [[1.],
     [0.]]
C = ctrb(A, B) # controlable

O = obsv(A, C)
print(linalg.det(O))  # no observable

# controlable y no observable

##### considerando solo U2

num7 = [(g*m*(bu-bv)*sin(2*theta))/20]
den7 = [20/20, 20200/20, 200500/20, 500000/20, 0 ,0]

Y1 = tf(1, den7)
print(Y1)

Y1ss = ss(Y1)

print(Y1ss)
A = [[-1.0100e+03 ,-1.0025e+04 ,-2.5000e+04 ,-0.0000e+00 ,-0.0000e+00],
     [ 1.0000e+00 , 0.0000e+00 , 0.0000e+00 , 0.0000e+00 , 0.0000e+00],
     [ 0.0000e+00 , 1.0000e+00 , 0.0000e+00 , 0.0000e+00 , 0.0000e+00],
     [ 0.0000e+00 , 0.0000e+00 , 1.0000e+00 , 0.0000e+00 , 0.0000e+00],
     [ 0.0000e+00 , 0.0000e+00 , 0.0000e+00 , 1.0000e+00 , 0.0000e+00]]
B = [[1.],
     [0.],
     [0.],
     [0.],
     [0.]]

C = ctrb(A, B)
O = obsv(A, C)
print(linalg.det(O))  # no observable

## controlable y no observable

#----------------------------------------------------------------------------------------------------------------------

#### th(s) depende de 1 entradas 

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

print(O)

# controlable y no observable
