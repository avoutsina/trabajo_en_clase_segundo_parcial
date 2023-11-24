import pygame
from soporte_file import *
from bloques import *


class Jugador(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.importar_assets_jugador()
        self.indice_frames = 0
        self.velocidad_animacion = 0.15
        self.image = self.animaciones["quieto"][self.indice_frames]
        self.rect = self.image.get_rect(midleft=(x,y))
        
        

        #movimientos del jugador
        self.direccion = pygame.math.Vector2(0,0) 
        self.velocidad = 5
        self.gravity = 0.8
        self.velocidad_salto = -18


        #player status
        self.que_hace = 'quieto'
        self.mirando_derecha = True
        self.piso = False
        self.techo = False
        self.izquierda = False
        self.derecha = False
     

  
    def importar_assets_jugador(self):
        character_path = r'tiles\personaje'
        self.animaciones = {'quieto':[],'correr':[],'salto':[],'caer':[],'salto_doble':[],'herido':[]}

        for animacion in self.animaciones.keys():
            path_completo = character_path +"\\"+ animacion
            self.animaciones[animacion] = import_carpeta(path_completo)

    def animate(self):
        animacion = self.animaciones[self.que_hace]

		 
        self.indice_frames += self.velocidad_animacion
        if self.indice_frames >= len(animacion):
            self.indice_frames = 0
            
        image = animacion[int(self.indice_frames)]
        if self.mirando_derecha:
            self.image = image
        else:
            imagen_volteada = pygame.transform.flip(image,True,False)
            self.image =  imagen_volteada

		
        if self.piso and self.derecha:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.piso and self.izquierda:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.piso:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.techo and self.derecha:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.techo and self.izquierda:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.techo:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def invertir_imagen(self):
        if self.velocidad > 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direccion.x = 1
            self.mirando_derecha = True
        elif keys[pygame.K_LEFT]:
            self.direccion.x = -1
            self.mirando_derecha = False
        else:
            self.direccion.x = 0

        if keys[pygame.K_SPACE] and self.piso:
            self.saltar()
        

    def obtener_estado(self):
        if self.direccion.y < 0:
            self.que_hace = 'salto'
        elif self.direccion.y > 1:
            self.que_hace = 'caer'
        else:
            if self.direccion.x != 0:
                self.que_hace = 'correr'
            else:
                self.que_hace = 'quieto'
    
    def aplicar_gravedad(self):
        self.direccion.y += self.gravity
        self.rect.y += self.direccion.y

    def saltar(self):
        self.direccion.y = self.velocidad_salto
    
    def update(self):
        self.get_input()
        self.obtener_estado()
        self.animate()
        
        