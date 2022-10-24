import pygame, sys

pygame.init()
clock = pygame.time.Clock()


## display surface 
screen = pygame.display.set_mode((800,800))
secon_surfes = pygame.Surface([100,200]) # display surface

secon_surfes.fill((0,255,0))

## foto

drone = pygame.image.load('uav.png')
drone_rect = drone.get_rect(topleft = [100,200])
print(drone_rect.center)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit ## end the program

    screen.fill((255,255,255)) #screen color
    screen.blit(secon_surfes,(0,50))
    screen.blit(drone,drone_rect)
    drone_rect.right +=5
    print(drone_rect.right)
        
    pygame.display.flip() ## visualizate everything
    clock.tick(60) ##frames

