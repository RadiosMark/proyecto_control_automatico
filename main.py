import pygame
import numpy as np
import time 
from scipy.integrate import odeint

from proyecto import dif_eq

g = 9.81
ti = 0

class UAV:
    def __init__(self):
        self.pos = [400, 400]
        self.theta = np.pi/2
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
         
        x1_d =x[3]*np.cos(x[2]) - x[4]*np.sin(x[2])
        x2_d = x[3]*np.sin(x[2]) + x[4]*np.cos(x[2])
        x3_d = x[5]
        x4_d = x[5]*x[4]+(1/self.masa)*(self.fr+self.fl)-(self.bu/self.masa)*x[3]-g*np.sin(x[2])
        x5_d = -x[5]*x[3]-(self.bv/self.masa)*x[4]-g*np.cos(x[2])
        x6_d = -(self.bw/self.iner)+(self.long_brazo/(2*self.iner))*(self.fr-self.fl)
        x_d = [x1_d,x2_d,x3_d,x4_d,x5_d,x6_d]
        return x_d
    
    def init(self):
        global ti
        Ts = time.time() -ti
        x = [self.pos[0],self.pos[1], self.theta, self.U, self.V, self.w]
        t = np.linspace(0, Ts, 2)
        ti = time.time()

        sol = odeint(dif_eq,x,t)
        self.pos[0] = sol[1][0]
        self.pos[1] = sol[1][1]
        self.theta = sol[1][2]
        self.U = sol[1][3]
        self.V = sol[1][4]
        self.w = sol[1][5]

    def update(self):
        pass


    def brazo_derecho(self):
        return(self.pos[0]-self.long_brazo*5, self.pos[1])

    def brazo_izquierdo(self):
        return(self.pos[0]+self.long_brazo*5, self.pos[1])

    def draw(self, dest):
        x = int(self.pos[0])
        y = int(self.pos[1])
        rx , ry = self.brazo_derecho()
        lx , ly = self.brazo_izquierdo()
        pygame.draw.line(dest, (255, 255, 255),(lx,ly),(rx,ry))
        pygame.draw.circle(dest, (255, 0, 0), (x, y), 10)
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulacion = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    uav.fl-=10
                    print("arriba")
                if event.key == pygame.K_s:
                    uav.pos[1]+=10
                    print("abajo")
                if event.key == pygame.K_d:
                    uav.pos[0]+=10
                    print("derecha")
                if event.key == pygame.K_a:
                    uav.pos[0]-=10
                    print("izquierda")
                uav.init() 
   
            ventana.fill((0,0,0))
            uav.draw(ventana)
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()

if __name__=="__main__":
    main()


     