import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Una clase para representar a un alienigena"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        
        #Cargando la imagen del enemigo y obtener su rectangulo
        self.image = pygame.image.load('images/fighter.png').convert_alpha()
        self.rect = self.image.get_rect()
        
        #Comenzar cada nuevo alienigena en la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Almacena la posicion horizontal exacta del alienigena
        self.x = float(self.rect.x)


