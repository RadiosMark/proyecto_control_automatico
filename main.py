import pygame
from numpy import *
import time 
from scipy.integrate import odeint

g = 9.81
ti = 0
time_scaling = 1.0

class UAV:
    def __init__(self, mira):
        self.pos = [400, 400]
        self.theta = pi/2
        self.long_brazo = 0.5
        self.masa = 10 #kg
        self.iner = 0.1
        self.V = 0
        self.U = 0
        self.w = 0
        self.bu = 50
        self.bv = 50
        self.bw = 100
        self.u1 = 10*g
        self.u2 = 0
        self.ti = 0
        self.mira = mira

    def dif_eq(self, x, t):

        ## calculamos los fr y fl
        nrow1 = [1, 1]
        nrow2 = [self.long_brazo/2, -self.long_brazo/2]
        matrix = array([nrow1, nrow2])
        cons = array([self.u1, self.u2])
        solution  = linalg.solve(matrix, cons)
        
        fr = solution[0]
        fl = solution[1]
        
        xd0 = x[3]*cos(x[2])-x[4]*sin(x[2])
        xd1 = x[3]*sin(x[2])+x[4]*cos(x[2])
        xd2 = x[5]
        xd3 = x[5]*x[4]+(1/self.masa)*(fr+fl)-((self.bu*x[3])/self.masa)-g*sin(x[2])
        xd4 = -x[5]*x[4]-((self.bv*x[4])/self.masa)-g*cos(x[2])
        xd5 = ((fr-fl)/(self.iner))-(self.bw/self.iner)*x[5]

        return multiply(time_scaling, [xd0, xd1, xd2, xd3, xd4, xd5])

    def init(self):

        Ts = time.time() - self.ti
        x = array([self.pos[0], self.pos[1], self.theta, self.U, self.V, self.w])
        t = linspace(0, Ts, 2)
        self.ti = time.time()


        sol = odeint(self.dif_eq, x, t)
        self.pos[0] = sol[-1, 0]
        self.pos[1] = sol[-1,1]
        self.theta = sol[-1,2]
        self.U = sol[-1,3]
        self.V = sol[-1,4]
        self.w = sol[-1,5]

    def brazo_derecho(self):
        x_d = sin(self.theta)
        y_d = cos(self.theta)
        return(self.pos[0]+x_d*self.long_brazo*50, (800-self.pos[1])+y_d*self.long_brazo*50)


    def brazo_izquierdo(self):
        x_d = sin(pi + self.theta)
        y_d = cos(pi + self.theta)
        return(self.pos[0]+x_d*self.long_brazo*50, (800-self.pos[1])+y_d*self.long_brazo*50)

    def draw(self, dest):

        x = self.pos[0]
        y = self.pos[1]
        rx , ry = self.brazo_derecho()
        lx , ly = self.brazo_izquierdo()
        pygame.draw.line(dest, (255, 255, 255),(lx,ly),(rx,ry))
        pygame.draw.circle(dest, (255, 0, 0), (x, (800-y)), 10)
        pygame.draw.circle(dest, (0, 255, 0), (lx, ly), 5)
        pygame.draw.circle(dest, (0, 0, 255), (rx, ry), 5)

        ### imprimer la mira
        self.mira.draw(dest)

    def freno_emergencia(self):
        self.u1 = 10*g
        self.u2 = 0
        self.theta = pi/2
        self.U = 0
        self.V = 0



class Mira():
    def __init__(self):
        self.pos = [200, 200]

    def draw(self, dest):
        pygame.draw.line(dest, (255,255,255), (self.pos[0]-20, self.pos[1]),(self.pos[0]+20, self.pos[1]))
        pygame.draw.line(dest, (255,255,255), (self.pos[0], self.pos[1]-20),(self.pos[0], self.pos[1]+20))

def main():
    pygame.init()
    clock = pygame.time.Clock()
    ventana = pygame.display.set_mode((800 ,800))
    simulacion = True

    mira = Mira()
    uav = UAV(mira)
    uav.init()
    while simulacion:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  ##  reconoce el input del mouse
                mira.pos[0] = event.pos[0]  #cambia la posición en x de la mira 
                mira.pos[1] = event.pos[1]  #cambia la posición en y de la mira 
            if event.type == pygame.QUIT:
                simulacion = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    uav.u1 +=2500
                if event.key == pygame.K_DOWN:
                    uav.u1 -=2500
                if event.key == pygame.K_LEFT:
                    uav.u2 +=20
                if event.key == pygame.K_RIGHT:
                    uav.u2 -= 20
                if event.key == pygame.K_s:
                    uav.freno_emergencia()

        uav.init()
        ventana.fill((0,0,0))
        uav.draw(ventana)
        pygame.display.flip()
        #clock.tick(60)
    pygame.quit()

if __name__=="__main__":
    main()


     