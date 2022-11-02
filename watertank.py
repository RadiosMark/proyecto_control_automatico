#------------------------------------------------------------------------------#
# Keyboard Input Using PyGame
# execute typing: python watertank.py
# http://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
# http://www.pygame.org/docs/ref/key.html
# http://www.tutorialspoint.com/python/python_numbers.htm
# https://docs.python.org/3/library/functions.html#int

# Program flow
# - Initialize state
# - Read user inputs
# - Step model
# - Draw stuff

import sys  # find ouf constants in sys.float_info
            # https://docs.python.org/2/library/sys.html#sys.float%5Finfo

import pygame
from pygame.locals import * # Must include this line to get the OpenGL
                            # definition otherwise importing just PyGame 
                            # is fine.

#import numpy as np
from numpy import *

import time

from scipy.integrate import odeint

import matplotlib.pyplot as plt


# --- Physics Variables --- 
# Controls
mv_user = 0 # This is the user set value for mv  (valve aperture in percent)
mv_out  = 0 # This is the physical value of the mv (valve aperture in area,  flow rate, or physical signal, e.g. driver current/voltage)
MV_USER_TO_OUT = 2.0 # Convert from 0-1 [%] to 0-2.0 [m3/s]
MV_USER_TO_REF = 1.0 # Convert from 0-1 [%] to 0-1.0 [m]
MV_OUT_MIN =  0.0 # [m3/s]
MV_OUT_MAX =  2.0 # [m3/s]


# State
level =  0.0
tempC = 20.0

TL_LO = 0.0 # Tank level low
TL_HI = 1.0 # Tank level high

# Reference
ref=0

# Model parameters
A_e = pi
A_s = pi*0.01**2
g = 9.81
c1 = 1/A_e
c2 = A_s*sqrt(2*g)/A_e

# Control mode
auto = 0

# Controller parameters and variables
Kp = 10.0
Ki = 5.0
Kd = 0
error      = 0
error_old  = 0
error_old2 = 0

# --- Simulation Variables ---

# Time counter for sampling time measurement
ti = 0

# Wall-clock time
tw0 = 0

# Simulation sampling time
Ts = 0.010      # This is just a reference value.  The current
                # simulation employs the real elapsed time,
                # i.e. variable sampling period Ts.

# Time scaling
time_scaling = 100.0

# Logger variables
k_data = 0              # Index to entry position of the data storage array
k_data_samples = 10000  # Number of data points to store. The time lenght of the buffer is k_data_samples*Ts ~= 10000*0.02 = 200 s.
record_size = 5        # Size of each record in the data array: time+state vector+referece+manipulated variable = 1+2+1+1
data = zeros((k_data_samples,record_size)) # Store in each row: time, state vector (row-wise), reference, manipulated variable 
#http://scipy.github.io/old-wiki/pages/NumPy_for_Matlab_Users.html


# --- Graphics Variables ---
XMAX = 640
YMAX = 480
screen = None

def store_data():
    # Store in row 'k' of the 'data' array of size (rows, cols)= (k_data_samples, size(t)+size(x)+size(ref)+size(mv))
    # the following values arranged column wise:
    # Time t, state x, referece ref and manipulated variables mv
    # Data is stored in a circular buffer, aka ring buffer or cyclic buffer
    global data, k_data_samples, k_data
    global tw0, level, tempC, ref, mv_out
    
    t = time.time()-tw0
    x = array([ level, tempC])
    #ref = level_ref
    mv  = mv_out
    
    data[k_data,:]=r_[t,r_[x,r_[ref,mv]]]
    k_data = k_data+1
    if k_data == k_data_samples:
        k_data = 0
        
def arrange_data():
    # Arrange the order of the data in the circular buffer from oldest to newest sample
    global data, k_data, k_data_samples
    
    if k_data>0:
        aux1 = data[:k_data,:]                      # Pick the first k_data values
        aux2 = data[-(k_data_samples-k_data):,:]    # Pick the remaining values in the data array
        data = r_[aux2,aux1]                        # Vertically stack the rows of aux2 and aux1
    # Check http://scipy.github.io/old-wiki/pages/NumPy_for_Matlab_Users.html
    # for info on array handling.
    
def update_display():
    state_str = 'Level: '+str(level)
    
    pygame.draw.rect(screen, (0,0,0) , screen.get_rect(), 0)
    #level_rnd = int(round(level,0))
    level_rnd = int(round((YMAX/2)*(level-TL_LO)/(TL_HI-TL_LO),0))
    pygame.draw.rect(screen, (0,255,255) , pygame.Rect(0,YMAX/2-level_rnd,XMAX,1+level_rnd), 0)
    #print screen.get_rect()
    font = pygame.font.SysFont('Arial', 25)
    screen.blit(font.render(state_str, True, (255,0,0)), (100, 100))
    pygame.display.flip()

# Manipulated variable
def u_fun(): #(ref,x):
    global ref, level, mv_user, mv_out
    global error_old, error_old2, Ts
    if auto == 0:
        mv_out = mv_user*MV_USER_TO_OUT
    if auto == 1:
        ref = mv_user*MV_USER_TO_REF
        error = ref-level
        mv_out = mv_out + Kp*(error-error_old) + Ki*Ts*error + Kd*(error-2*error_old+error_old2)/Ts
        if mv_out > MV_OUT_MAX:
            mv_out = MV_OUT_MAX
        elif mv_out < MV_OUT_MIN:
            mv_out = MV_OUT_MIN
        error_old2 = error_old
        error_old = error
    return mv_out

def check_state_bounds():
    global level, tempC # State variables
    global TL_LO, TL_HI # State bounds
    
    if level > TL_HI:   # Check level bounds
        level = TL_HI
    if abs(level-TL_LO) < sys.float_info.epsilon*1e10:
        level = TL_LO

multiply

# State model
# xd = f(x,u)
# dV/dt = Q - A_s\sqrt{2gh}
# V=A_e*h -> dV/dt =A_e*dh/dt
# dh/dt = Q/A_e - (A_s\sqrt{2g}/A_e)\sqrt{h}
def xd_fun(x, t):
   global mv_out
   # u = u_fun(ref,x) 
   u = mv_out
   
   xd0 = c1*u/YMAX - c2*sqrt(abs(x[0]))
   xd1 = c1*x[0] - c2*x[1]
   return multiply(time_scaling,[xd0, xd1])
   
def update_state():
    global level, tempC # State variables
    global ti, Ts
   
    x0 = array([level, tempC])  # Current state is the initial state for
                                # an integration step

    mv_out = u_fun()                            
                                
    # Ts = 0.01
    #Ts = time.perf_counter() - ti # elapsed CPU time... the time dedicated by the CPU to the process, aka execution time or processor time
    Ts = time.time() - ti # elapsed wall-clock time... the time it takes to run the process, aka elapsed time or running time
    #print("Sampling time Ts is %f" %Ts)
    
    t = linspace(0.0, Ts, 2)
    x = odeint(xd_fun, x0, t)   # Perform integration using Fortran's LSODA (Adams & BDF methods)

    level = x[-1,0] # Gets the last row of x and first column
    tempC = x[-1,1] # Gets the last row of x and second column
                    # Repeat this for all the state variables
       
    check_state_bounds()
    
    #x[-1,0] = level    # Update the initial state for next iteration
    #x0 = x[-1,:]       # This is not necessary as it is done at the beginning
                        # of this function

    
    #ti = time.perf_counter()
    ti = time.time()
    
def keyboard_logic(key):
    global mv_user
    
    if key == pygame.K_DOWN:
        mv_user-=0.1
        if mv_user < 0:
            mv_user=0
            if auto == 0:
                print("Valve is fully closed!")
            else:
                print("Mininum reference value reached!")
        else:
            if auto == 0:
                print("Closing valve to: %f [percent] (%f [m3/s])" %(mv_user, mv_user*MV_USER_TO_OUT))
            else:
                print("Decreasing reference level to: %f [percent] (%f [m3/s])" %(mv_user, mv_user*MV_USER_TO_REF))
    if key == pygame.K_UP:
        mv_user+=0.1
        if mv_user > 1:
            mv_user=1
            if auto == 0:
                print("Valve is fully open!")
            else:
                print("Maximum reference value reached!")
        else:
            if auto == 0:
                print("Opening valve to: %f [percent] (%f [m3/s])" %(mv_user, mv_user*MV_USER_TO_OUT))
            else:
                print("Increasing reference level to: %f [percent] (%f [m3/s])" %(mv_user, mv_user*MV_USER_TO_REF))
    
def handle_keyboard():
    global time_scaling, auto, mv_user, ref
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUITis sent when the user clicks the window's "X" button, or when the system 'asks' for the process to quit
                                       # http://stackoverflow.com/questions/10080715/pygame-event-event-type-pygame-quit-confusion
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:    # http://www.pygame.org/docs/ref/key.html
            if    event.key == pygame.K_UP \
               or event.key == pygame.K_DOWN:
                keyboard_logic(event.key)
            if event.key == pygame.K_a:   
                auto = 1
                ref = level # Make reference equal to the current state when
                            # switching from  manual to auto.
                mv_user = ref/MV_USER_TO_REF
                print("\nControl mode is set to [automatic]")
                print("Reference is %f" %ref)
            if event.key == pygame.K_m:
                auto = 0
                print("\nControl mode is set to [manual]")    
            if event.key == K_s:
                arrange_data()
                save("simdata.npy",data)
                print("File saved to 'simdata.npy'")
                #savetxt("simdata.csv",data)
                #print("File saved to 'simdata.csv'")
    return True

def init_display():
    global XMAX, YMAX, screen
    
    # Initialize PyGame and setup a PyGame display
    pygame.init()
    # pygame.display.set_mode()
    screen = pygame.display.set_mode((XMAX,YMAX))
    pygame.display.set_caption('Watertank Sim')
    pygame.key.set_repeat(1,50)     # Works with essentially no delay.
    #pygame.key.set_repeat(0,50)    # Doesn't work because when the delay
                                    # is set to zero, key.set_repeat is
                                    # returned to the default, disabled
                                    # state.
    
def main():
    global tw0, XMAX, YMAX, screen

    # Initialize time counter
    tw0 = time.time()
    
    init_display()
    

                             
    while True:

        handle_keyboard()
        update_state()
        update_display()
        store_data()

        #pygame.time.wait(10) # Set a wait-time to delay capture from keyboard to 10 miliseconds
                             # For very fast processes, it may be necessary to slow down the keyboard 
                             # capture rate in order to reduce fast/abrubpt responses. However, beware
                             # that this delay also reduces the sampling time of the simulator.
                             # Without this delay, the sampling time is on average 8 ms, with the
                             # 10 ms delay, the sampling time increase to 18 ms.
                
if __name__ == '__main__': main()