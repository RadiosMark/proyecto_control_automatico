from array import array
from cmath import rect
from turtle import position
import pygame, sys
from scipy.integrate import odeint
from numpy import *

def der_x(U,V,theta): return U*(np.cos(theta))- V*(np.sin(theta))


### Define Eq Values

theta0 = 0

x1 = 0 # x pos
x2 = 0  # y pos
x3 = pi/2 # theta
x4 = 0 # U 
x5 = 0 # V
x6 = 0 # w

x = [x3,x4,x5,x6]

#constants
m = 10
bu = 50 #N/(m/s)
bv = 50 #N/(m/s)
bw = 100 #Nm/(rad/s)
g = 9.81
l = 0.5
I = 0.1 #kgm2

# time

ti = 0.0
Ts = 0.010
t = linspace(ti, Ts, 2)

# control_variables

fl = 0
fr = 0

## ecuations

def dif_eq(x, t):
    global bw, bv, bu, g, I, l, fl, fr, m

    x0_d = x[3] # theta 0
    x1_d = x[3]*x[2]+(1/m)*(fr+fl)-(bu/m)*x[1]-g*sin(x[0]) # u 1
    x2_d = -x[3]*x[1]-(bv/m)*x[2]-g*cos(x[0]) # v 2
    x3_d = -(bw/I)*(x0_d)+(l/(2*I))*(fr-fl) # omega 3
    x_d = [x0_d,x1_d,x2_d, x3_d]
    return x_d

sol_x = odeint(dif_eq , x , t)
print(sol_x)



### make the drone 









#pygame.init()
#clock = pygame.time.Clock()


## display surface 
#screen = pygame.display.set_mode((800,800))
#secon_surfes = pygame.Surface([100,200]) # display surface
#Rect = pygame.draw.ellipse(secon_surfes, (0,0,0), rect(2,7) )

#secon_surfes.fill((0,255,0))

#scipy.integrate.odeint

## foto

#drone = pygame.image.load('uav.png')
#drone_rect = drone.get_rect( center = [0,400])
#print(drone_rect.center)

#while True:
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT:
            #pygame.quit()
            #sys.exit ## end the program

    #screen.fill((255,255,255)) #screen color
    #screen.blit(elip,(100,100))
    #screen.blit(drone,drone_rect)
        
    #pygame.display.flip() ## visualizate everything
    #ad ##frames


 