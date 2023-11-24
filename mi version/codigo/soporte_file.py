import pygame
import csv
from csv import reader
from config import *
from os import walk


def import_carpeta(path):
    lista_superficies = []

    for _,__,imagenes in walk(path):
        for imagen in imagenes:
            path_completo = path + "\\"+ imagen
            imagen_surface = pygame.image.load(path_completo).convert_alpha()
            imagen_surface = pygame.transform.scale(imagen_surface,((imagen_surface.get_width()*2),(imagen_surface.get_height())*2))
            lista_superficies.append(imagen_surface)
    return lista_superficies


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for fila in level:
            terrain_map.append(list(fila))
        return terrain_map

def import_imagen_fraccionada(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width() / tamanio_tiles)
    tile_num_y = int(surface.get_height() / tamanio_tiles)

    lista_fracciones = []
    for fila in range (tile_num_y):
        for columna in range(tile_num_x):
            x = columna * tamanio_tiles
            y = fila * tamanio_tiles
            nueva_surface = pygame.Surface((tamanio_tiles, tamanio_tiles))
            nueva_surface.blit(surface,(0,0),pygame.Rect(x,y,tamanio_tiles,tamanio_tiles))
            lista_fracciones.append(nueva_surface)
    return lista_fracciones


