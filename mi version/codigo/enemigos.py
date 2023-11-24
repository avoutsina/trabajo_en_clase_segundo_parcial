import pygame
from soporte_file import *
from bloques import *
from random import randint

class Enemigo(TileAnimado):
    def __init__(self, tamanio_tiles, x, y):
        super().__init__(tamanio_tiles, x, y, r"tiles\enemigos\correr")
        self.rect.y += tamanio_tiles - self.image.get_height()+5
        self.velocidad = randint(1,4)
    def animar(self):
        self.indice_frames += 0.2
        if self.indice_frames >= 5:
            self.indice_frames = 0
        self.image = self.frames[int(self.indice_frames)]
    
    def mover(self):
        self.rect.x += self.velocidad 
    
    def invertir_imagen(self):
        if self.velocidad > 0:
            self.image = pygame.transform.flip(self.image,True,False)
        
    def reversa(self):
        self.velocidad *= -1
    
    def update(self):
        self.animar()
        self.mover()
        self.invertir_imagen()
        