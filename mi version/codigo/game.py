import pygame, sys
from config import *
from level import Level
from data import *
from modo import *

pygame.init()

FPS = 60
PANTALLA = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
nivel_1 = Level(level_1, PANTALLA,r"tiles\fondo\fondo_lvl_1.png")

corriendo = True

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                cambiar_modo()
    
    nivel_1.run( )

    pygame.display.update()
    clock.tick(FPS)