import pygame
from numpy import *
import time 
from scipy.integrate import odeint


# definimos variables globales
g = 9.81
ti = 0
time_scaling = 1.0
txt = 'ejemplo.txt'
U1 = []
U2 = []
X = []
Y = []
Theta = []

class UAV:  #------------------- se define la clase del drone UAV con sus parámetros (la mayoria por enunciado/punto de equilibrio) --------------------------
    def __init__(self, mira, ruta):
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

        ## suave
        self.suave_u1 = False
        self.suave_u2 = False

        ## parámetros para modo automático
        self.auto = False
        self. llego_vertical = False
        self.llego_horizontal = False
        self.vertical = 'Arriba'
        self.horizontal = 'Izquierda'
        self.counter = False

        #trayectoria
        self.trayecto = False
        self.ruta = ruta
        self.camino = []
        self.lugar_lista = 0

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

    def freno_suave(self):
        if self.u1 > 0:
            self.u1 -=(2500+self.masa*g) 
        elif self.u1 < 0:
            self.u1 +=(2500-self.masa*g) 
        if -10 <self.u1 < 10:
            self.u1 = self.masa*g
            self.suave_u1 = False
        
        if sin(pi + self.theta)> 0 and cos(pi + self.theta)< 0:
            self.u2 += 20
        elif sin(pi + self.theta)> 0 and cos(pi + self.theta) > 0:
            self.u2 -= 20
        if -0.01 <cos(self.theta) < 0.01:
            self.u2 = 0
            self.u1 = self.masa*g
            self.suave_u2 = False

    
    def automatico(self):  # en proceso
        if self.llego_vertical == False or self.llego_horizontal == False:
            if (800-self.pos[1]) > (self.mira.pos[1]) and self.vertical == 'Arriba' and self.llego_vertical == False :
                self.u1 =+1500
            if (800-self.pos[1]) < (self.mira.pos[1]) and self.vertical == 'Arriba':
                self.llego_vertical = True
                #self.freno_suave()
            if (800-self.pos[1]) -100 < (self.mira.pos[1]) and self.vertical == 'Abajo' and self.llego_vertical == False :
                self.freno_suave()
                self.u1 = -1500
            if (800-self.pos[1]) -100 > (self.mira.pos[1]) and self.vertical == 'Abajo':
                self.freno_suave()
                self.vertical = 'Arriba'
                if self.mira.pos[0] < self.pos[0]:
                    self.horizontal = 'Izquierda'
                    self.u2 += 15
                elif self.mira.pos[0] > self.pos[0]:
                    self.horizontal = 'Derecha'
                    self.u2 -= 15
            if self.theta > arctan((self.pos[1]-self.mira.pos[1])/(+self.mira.pos[0]-self.pos[0])) and self.horizontal == 'Derecha' and self.vertical == 'Arriba' and self.llego_horizontal == False:
                self.u2 -= 10
                print("porque no entra aquí")
            if self.theta < arctan((self.pos[1]-self.mira.pos[1])/(+self.mira.pos[0]-self.pos[0])) and self.horizontal == 'Derecha' and self.vertical == 'Arriba' and self.llego_horizontal == False:
                self.u2 = 0
            if self.theta < arctan((-self.mira.pos[0]+self.pos[0])/(self.pos[1]-self.mira.pos[1])) + pi/2 and self.horizontal == 'Izquierda'and self.vertical == 'Arriba'  and self.llego_horizontal == False:
                self.u2 += 10
                print("porque no entra aquí")
            if self.theta > arctan((-self.mira.pos[0]+self.pos[0])/(self.pos[1]-self.mira.pos[1])) + pi/2  and self.horizontal == 'Izquierda' and self.vertical == 'Arriba' and self.llego_horizontal == False:
                self.u2 = 0
            
   
    def añadir_lista(self):  ### metodo para añadir la lista con objetivos Ej: [[120, 0], [34, 50], [17, 300]]
        with open(self.ruta, 'r', encoding='utf-8') as file:
            lineas = file.read().splitlines()
            for linea in lineas:
                linea = linea.split(',')
                self.camino.append([int(linea[0]), int(linea[1])]) #queda guardada dentro de la variable del objeto.
    
    def recorrido(self):
        self.pos[0] = self.camino[self.lugar_lista][0]
        self.pos[1] = self.camino[self.lugar_lista][1]
        self.lugar_lista+= 1
        print(self.pos)
        if self.lugar_lista == len(self.camino):
            self.trayecto = False
        

class Mira(): #definimos el objeto mira; que se relaciona con el modo automático del UAV
    def __init__(self):
        self.pos = [200, 200]

    def draw(self, dest):
        pygame.draw.line(dest, (255,255,255), (self.pos[0]-20, self.pos[1]),(self.pos[0]+20, self.pos[1]))
        pygame.draw.line(dest, (255,255,255), (self.pos[0], self.pos[1]-20),(self.pos[0], self.pos[1]+20))
    
    
def main(): ## desde aquí se ejecuta el programa
    pygame.init()
    ventana = pygame.display.set_mode((800 ,800)) #ventana de 800p por 800p
    simulacion = True # condicion de simulación para el while

    mira = Mira() #instanciamos mira
    uav = UAV(mira,txt) #instanciamos nuestro UAV
    uav.añadir_lista()
    uav.init() # incializamos las condiciones iniciales
    while simulacion:
        for event in pygame.event.get():  # inputs del teclado / mouse
            if event.type == pygame.MOUSEBUTTONDOWN:  ##  reconoce el input del mouse
                mira.pos[0] = event.pos[0]  #cambia la posición en x de la mira 
                mira.pos[1] = event.pos[1]  #cambia la posición en y de la mira 
                uav.llego_vertical = False
                uav.llego_horizontal = False
                if mira.pos[1] < (800 - uav.pos[1]):
                    uav.vertical = 'Arriba'
                if mira.pos[1] > (800 - uav.pos[1]):
                    uav.vertical = 'Abajo'
                if mira.pos[0] < uav.pos[0]:
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
                if event.key == pygame.K_a:
                        uav.auto = True
                        print("Auto Mode Activado")
                        uav.llego_vertical = False
                        uav.llego_horizontal = False
                        if mira.pos[1] < (800 - uav.pos[1]):
                            uav.vertical = 'Arriba'
                        if mira.pos[1] > (800 - uav.pos[1]):
                            uav.vertical = 'Abajo'
                        if mira.pos[0] < uav.pos[0]:
                            uav.horizontal = 'Izquierda'
                        if mira.pos[0] > uav.pos[0]:
                            uav.horizontal = 'Derecha'
                
                if event.key == pygame.K_s:
                    uav.suave_u1 = True
                    uav.suave_u2 = True


        if uav.suave_u1 or uav.suave_u2:
            uav.freno_suave()
        if uav.auto:
            uav.automatico()

        uav.init() # actualiza las componentes del UAV
        ventana.fill((0,0,0))
        uav.draw(ventana) #dibuja el UAV en la pantalla
        pygame.display.flip()
    pygame.quit()

if __name__=="__main__":
    main()


     