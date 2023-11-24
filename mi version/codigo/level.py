import pygame
from soporte_file import *
from config import *
from bloques import *
from enemigos import *
from jugador import *
from modo import *



class Level:
    def __init__(self, level_data, surface, path_fondo):
        #General
        self.display_surface = surface
        self.fondo = pygame.transform.scale(pygame.image.load(path_fondo),(WIDTH, HEIGHT))
        
        #Jugador
        jugador_layout = import_csv_layout(level_data['jugador'])
        self.jugador = pygame.sprite.GroupSingle()
        self.jugador_setups(jugador_layout)
        self.jugador_en_el_piso = False

        #Terreno
        terreno_layout= import_csv_layout(level_data["terreno"])
        self.terreno_sprites = self.crear_grupo_tiles(terreno_layout,"terreno")

        #Items
        items_layout= import_csv_layout(level_data["items"])
        self.items_sprites = self.crear_grupo_tiles(items_layout,"items")

        #Trampas
        trampas_layout= import_csv_layout(level_data["trampas"])
        self.trampas_sprites = self.crear_grupo_tiles(trampas_layout,"trampas")


        #Enemigos
        enemigos_layout= import_csv_layout(level_data["enemigos"])
        self.enemigos_sprites = self.crear_grupo_tiles(enemigos_layout,"enemigos")
        
        #Limites enemigos
        limites_layout= import_csv_layout(level_data["limites"])
        self.limites_sprites = self.crear_grupo_tiles(limites_layout,"limites")

    def blitear_bordes(self):
        for bordes in self.bordes:
            self.display_surface.blit(bordes,(0,0))

    def crear_grupo_tiles(self,layout,type):
        grupo_sprites = pygame.sprite.Group()

        for indice_fila, fila in enumerate(layout):
            for indice_columna, bloque in enumerate(fila):
                if bloque != "-1":
                    x = indice_columna * tamanio_tiles
                    y = indice_fila * tamanio_tiles

                    if type == "terreno":
                        lista_terrenos_tiles = import_imagen_fraccionada(r"tiles\terreno\pasto - Copy.png")
                        tile_surface = lista_terrenos_tiles[int(bloque)]
                        sprite = TileEstatica(tamanio_tiles, x, y, tile_surface)
                    
                    if type == "items":
                        if bloque == "0":
                            sprite = Platita(tamanio_tiles, x, y, r"tiles\items\platita")
                        elif bloque =="1":
                            sprite = Vida(tamanio_tiles, x, y, r"tiles\items\vida")
                        else:
                            sprite = Power_up(tamanio_tiles, x, y, r"tiles\items\power_up")
                    
                    if type == "trampas":
                        sprite = Trampa(tamanio_tiles, x, y, r"tiles\trampas\trampa_fuego")
                    
                    if type == "enemigos":
                        if bloque == "0":
                            sprite = Enemigo(tamanio_tiles, x, y)
                        
                    if type == "limites":
                        sprite = Tile(tamanio_tiles,x ,y)
                        
                    grupo_sprites.add(sprite)
           
        return grupo_sprites

    def jugador_setups(self,layout):
        for indice_fila, fila in enumerate(layout):
            for indice_columna, valor in enumerate(fila):
                x = indice_columna * tamanio_tiles
                y = indice_fila * tamanio_tiles
                if valor == "0":
                    sprite = Jugador(x,y)
                    self.jugador.add(sprite)
            

    def colision_enemigo_limites(self):
        for enemigo in self.enemigos_sprites.sprites():
            if pygame.sprite.spritecollide(enemigo,self.limites_sprites,False):
                enemigo.reversa()

    def colision_movimentos_horizontal(self):
        jugador = self.jugador.sprite
        jugador.rect.x += jugador.direccion.x * jugador.velocidad
        print(jugador.rect)
        sprites_colicionables = self.terreno_sprites.sprites()
        for sprite in sprites_colicionables:
            if sprite.rect.colliderect(jugador.rect):
                if jugador.direccion.x < 0: 
                    jugador.rect.left = sprite.rect.right
                    jugador.izquierda = True
                    self.x_actual = jugador.rect.left
                elif jugador.direccion.x > 0:
                    jugador.rect.right = sprite.rect.left
                    jugador.derecha = True
                    self.x_actual = jugador.rect.right
        if jugador.rect.x <= -23:
            jugador.rect.x = -23
        elif jugador.rect.x >= 1240:
            jugador.rect.x = 1240

                    
        if jugador.izquierda and (jugador.rect.left < self.x_actual or jugador.direccion.x >= 0):
            jugador.izquierda = False
        if jugador.derecha and (jugador.rect.right > self.x_actual or jugador.direccion.x <= 0):
            jugador.derecha = False

    def colision_movimentos_vertical(self):
        jugador = self.jugador.sprite
        jugador.aplicar_gravedad()
        sprites_colicionables = self.terreno_sprites.sprites()
        
        for sprite in sprites_colicionables:
            if sprite.rect.colliderect(jugador.rect):
                if jugador.direccion.y > 0: 
                    jugador.rect.bottom = sprite.rect.top
                    jugador.direccion.y = 0
                    jugador.piso = True
                elif jugador.direccion.y < 0:
                    jugador.rect.top = sprite.rect.bottom
                    jugador.direccion.y = 0
                    jugador.techo = True

        if jugador.piso and jugador.direccion.y < 0 or jugador.direccion.y > 1:
            jugador.piso = False
        if jugador.techo and jugador.direccion.y > 0.1:
            jugador.techo = False

    def poner_jugador_en_el_piso(self):
        if self.jugador.sprite.piso:
            self.jugador_en_el_piso = True
        else:
            self.jugador_en_el_piso = False


    def run(self):
        #que corra el nivel
        self.display_surface.blit(self.fondo,(0,0))

        self.terreno_sprites.draw(self.display_surface)
        
        self.jugador.update()
        self.colision_movimentos_horizontal()
        self.poner_jugador_en_el_piso()
        self.colision_movimentos_vertical()
        self.jugador.draw(self.display_surface)

        self.items_sprites.update()
        self.items_sprites.draw(self.display_surface)

        self.trampas_sprites.update()
        self.trampas_sprites.draw(self.display_surface)
        
        self.enemigos_sprites.update()   
        self.limites_sprites.update()
        self.colision_enemigo_limites()
        self.enemigos_sprites.draw(self.display_surface)
        if obtener_modo():
            #Borde_izquierdo
            pygame.draw.line(self.display_surface, "red", (0,0), (0,HEIGHT))
            #Borde_derecho
            pygame.draw.line(self.display_surface, "red", (WIDTH-1,0), (WIDTH-1,HEIGHT))
            #Borde_superior
            pygame.draw.line(self.display_surface, "red", (0,0), (WIDTH,0))
            #Borde_inferior
            pygame.draw.line(self.display_surface, "red", (0,HEIGHT-1), (WIDTH,HEIGHT-1))
        