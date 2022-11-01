import pygame


class UAV:
    def __init__(self):
        self.pos = [400, 400]
        self.long_brazo = 5

    def brazo_derecho(self):
        return(self.pos[0]-self.long_brazo*5, 400)

    def brazo_izquierdo(self):
        return(self.pos[0]+self.long_brazo*5, 400)

    def draw(self, dest):
        x = int(self.pos[0])
        y = int(self.pos[1])
        rx , ry = self.brazo_derecho()
        lx , ly = self.brazo_izquierdo()
        pygame.draw.line(dest, (255, 255, 255),(lx,ly),(rx,ry))
        pygame.draw.circle(dest, (255, 0, 0), (x, y), 10)
        pygame.draw.circle(dest, (0, 255, 0), (lx, ly), 5)
        pygame.draw.circle(dest, (0, 0, 255), (rx, ry), 5)

    def update(self):
        pass


def main():
    pygame.init()
    clock = pygame.time.Clock()
    ventana = pygame.display.set_mode((800 ,800))
    simulacion = True

    uav = UAV()
    while simulacion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulacion = False
            if event.type == pygame.K_UP:
                uav.pos[1]+=10
            if event.type == pygame.K_DOWN:
                uav.pos[1]-=10
            if event.type == pygame.K_RIGHT:
                uav.pos[0]+=10
            if event.type == pygame.K_LEFT:
                uav.pos[0]-=10
    
            ventana.fill((0,0,0))
            uav.draw(ventana)
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()

if __name__=="__main__":
    main()


     