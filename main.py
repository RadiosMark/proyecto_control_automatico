import pygame
from numpy import *
import time 
from scipy.integrate import odeint


# definimos variables globales
g = 9.81
ti = 0
time_scaling = 1.0

class UAV:  #------------------- se define la clase del drone UAV con sus parámetros (la mayoria por enunciado/punto de equilibrio) --------------------------
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

        ## parámetros para modo automático
        self.auto = False
        self. llego_vertical = False
        self.llego_horizontal = False
        self.vertical = 'Arriba'
        self.horizontal = 'Izquierda'
        self.counter = False

    def dif_eq(self, x, t):  ## se define el sistema de edos que se ocupará en el comando de odeint

        ## calculamos los fr y fl dados u1 y u2
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

    def init(self): ## este es el metodo por defecto que inicializa y actualiza la posción de 'x' e 'y' y 'theta'

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

    def brazo_derecho(self):  # manejo de la posición del brazo derecho del uav
        x_d = sin(self.theta)
        y_d = cos(self.theta)
        return(self.pos[0]+x_d*self.long_brazo*50, (800-self.pos[1])+y_d*self.long_brazo*50)


    def brazo_izquierdo(self): # manejo de la posición del izqyuierdo derecho del uav
        x_d = sin(pi + self.theta)
        y_d = cos(pi + self.theta)
        return(self.pos[0]+x_d*self.long_brazo*50, (800-self.pos[1])+y_d*self.long_brazo*50)

    def draw(self, dest): # se dibuja UAV con sus brazos y la mira

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

    def freno_emergencia(self): ## dejá todo en el punto de equilibrio
        self.u1 = 10*g
        self.u2 = 0
        self.theta = pi/2
        self.U = 0
        self.V = 0
    
    def automatico(self):  # en proceso
        if self.llego_vertical == False or self.llego_vertical == False:
            if (800-self.pos[1]) > (self.mira.pos[1]) and self.vertical == 'Arriba':
                self.u1 = 1000
            if (800-self.pos[1]) < (self.mira.pos[1]) and self.vertical == 'Arriba':
                self.llego_vertical = True
            if (800-self.pos[1]) < (self.mira.pos[1]) and self.vertical == 'Abajo':
                self.u1 = -1000
            if (800-self.pos[1]) > (self.mira.pos[1]) and self.vertical == 'Abajo':
                self.llego_vertical = True
            if self.pos[0] > self.mira.pos[0] and self.horizontal == 'Izquierda' and self.vertical == 'Abajo':
                if self.pos[0] - self.mira.pos[0] < 10:
                    self.u2 = 10
                    print("estabilizando")
                elif self.counter == False:
                    self.u2 =-30
                    self.counter = True
                elif self.counter == True:
                    self.u2 = 25
                    self.counter = False    
            elif self.pos[0] > self.mira.pos[0] and self.horizontal == 'Izquierda':
                if self.pos[0] - self.mira.pos[0] < 10:
                    if self.counter == False:
                        self.u2 = 10
                    elif self.counter == True:
                        self.u2 = -5
                    print("estabilizando")
                elif self.counter == False:
                    self.u2 =30
                    self.counter = True
                elif self.counter == True:
                    self.u2 = -25
                    self.counter = False
            if self.pos[0] < self.mira.pos[0] and self.horizontal == 'Izquierda':
                self.llego_horizontal = True
            if self.pos[0] < self.mira.pos[0] and self.horizontal == 'Derecha':
                if self.mira.pos[0] - self.pos[0] < 10:
                    self.u2 = 10
                    print("estabilizando")
                elif self.counter == False:
                    self.u2 =-30
                    self.counter = True
                elif self.counter == True:
                    self.u2 = 25
                    self.counter = False
            if self.pos[0] > self.mira.pos[0] and self.horizontal == 'Derecha':
                self.llego_horizontal = True
        elif self.llego_horizontal== True and self.llego_vertical == True:
            self.freno_emergencia()
            print("llegamos")
        


class Mira(): #definimos el objeto mira; que se relaciona con el modo automático del UAV
    def __init__(self):
        self.pos = [200, 200]

    def draw(self, dest):
        pygame.draw.line(dest, (255,255,255), (self.pos[0]-20, self.pos[1]),(self.pos[0]+20, self.pos[1]))
        pygame.draw.line(dest, (255,255,255), (self.pos[0], self.pos[1]-20),(self.pos[0], self.pos[1]+20))

def main(): ## desde aquí se ejecuta el programa
    pygame.init()
    clock = pygame.time.Clock()
    ventana = pygame.display.set_mode((800 ,800)) #ventana de 800p por 800p
    simulacion = True # condicion de simulación para el while

    mira = Mira() #instanciamos mira
    uav = UAV(mira) #instanciamos nuestro UAV
    uav.init() # incializamos las condiciones iniciales
    conteo = 0
    while simulacion:
        for event in pygame.event.get():  # inputs del teclado / mouse
            if event.type == pygame.MOUSEBUTTONDOWN:  ##  reconoce el input del mouse
                mira.pos[0] = event.pos[0]  #cambia la posición en x de la mira 
                mira.pos[1] = event.pos[1]  #cambia la posición en y de la mira 
                uav.llego_vertical = False
                uav.llego_horizontal = False
                if mira.pos[1] < (800 - uav.pos[1]):
                    uav.vertical = 'Arriba'
                    print(uav.vertical)
                if mira.pos[1] > (800 - uav.pos[1]):
                    uav.vertical = 'Abajo'
                    print(uav.vertical)
                if mira.pos[0] <uav.pos[0]:
                    uav.horizontal = 'Izquierda'
                if mira.pos[0] > uav.pos[0]:
                    uav.horizontal = 'Derecha'
            if event.type == pygame.QUIT:
                simulacion = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and uav.auto == False:
                    uav.u1 +=2500
                if event.key == pygame.K_DOWN and uav.auto == False:
                    uav.u1 -=2500
                if event.key == pygame.K_LEFT and uav.auto == False:
                    uav.u2 +=20
                if event.key == pygame.K_RIGHT and uav.auto == False:
                    uav.u2 -= 20
                if event.key == pygame.K_s:
                    uav.freno_emergencia()
                if event.key == pygame.K_a:
                    if conteo == 0:
                        uav.auto = True
                        print("Auto Mode Activado")
        
        if uav.auto:
            uav.automatico()

        uav.init() # actualiza las componentes del UAV
        ventana.fill((0,0,0))
        uav.draw(ventana) #dibuja el UAV en la pantalla
        pygame.display.flip()
    pygame.quit()

if __name__=="__main__":
    main()


     