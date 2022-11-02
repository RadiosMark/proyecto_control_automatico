import pygame
from numpy import *
import time 
from scipy.integrate import odeint
from proyecto import dif_eq

g = 9.81
ti = 0
time_scaling = 100.0

class UAV:
    def __init__(self):
        self.pos = [400, 400]
        self.theta = pi/2
        self.long_brazo = 5
        self.masa = 10 #kg
        self.iner = 0.1
        self.V = 0
        self.U = 0
        self.w = 0
        self.bu = 50
        self.bv = 50
        self.bw = 100
        self.fl = 0
        self.fr = 0


    def dif_eq(self, x, t):
        
        xd0 = x[3]*cos(x[2]) - x[4]*sin(x[2])
        xd1 = x[3]*sin(x[2]) + x[4]*cos(x[2])
        xd2 = x[5]
        xd3 = x[5]*x[4]+(1/self.masa)*(self.fr+self.fl)-(self.bu/self.masa)*x[3]-g*sin(x[2])
        xd4 = -x[5]*x[3]-(self.bv/self.masa)*x[4]-g*cos(x[2])
        xd5 = -(self.bw*x[5]/self.iner)+((self.long_brazo*10)/(2*self.iner))*(self.fr-self.fl)

        return multiply(time_scaling , [xd0 ,xd1 ,xd2 ,xd3 ,xd4 ,xd5])
    
    def init(self):
        global ti
        Ts = time.time() - ti
        x = array([self.pos[0], self.pos[1], self.theta, self.U, self.V, self.w])
        t = linspace(0, Ts, 2)
        ti = time.time()
        print("el tiempo es", Ts)

        sol = odeint(dif_eq, x, t)
        print(sol[-1])
        self.pos[0] = sol[-1, 0]
        self.pos[1] = sol[-1,1]
        self.theta = sol[-1,2]
        self.U = sol[-1,3]
        self.V = sol[-1,4]
        self.w = sol[-1,5]

    def update(self):
        pass

    def brazo_derecho(self):
        return(self.pos[0]-self.long_brazo*5, (800-self.pos[1]))

    def brazo_izquierdo(self):
        return(self.pos[0]+self.long_brazo*5, (800-self.pos[1]))

    def draw(self, dest):
        x = self.pos[0]
        y = self.pos[1]
        rx , ry = self.brazo_derecho()
        lx , ly = self.brazo_izquierdo()
        pygame.draw.line(dest, (255, 255, 255),(lx,ly),(rx,ry))
        pygame.draw.circle(dest, (255, 0, 0), (x, (800-y)), 10)
        pygame.draw.circle(dest, (0, 255, 0), (lx, ly), 5)
        pygame.draw.circle(dest, (0, 0, 255), (rx, ry), 5)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    ventana = pygame.display.set_mode((800 ,800))
    simulacion = True

    uav = UAV()
    uav.init()
    while simulacion:
        uav.init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulacion = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    uav.fl=100
                    uav.fr=200
                if event.key == pygame.K_s:
                    uav.pos[1]+=10
                    print("abajo")
                if event.key == pygame.K_d:
                    uav.pos[0]+=10
                    print("derecha")
                if event.key == pygame.K_a:
                    uav.pos[0]-=10
                    print("izquierda")

            
            ventana.fill((0,0,0))
            uav.draw(ventana)
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()

if __name__=="__main__":
    main()


     