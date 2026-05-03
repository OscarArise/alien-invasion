import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Una clase para representar a un alienigena"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        #Cargando la imagen del enemigo y obtener su rectangulo
        self.image = pygame.image.load('images/fighter.png').convert_alpha()
        self.rect = self.image.get_rect()
        
        #Comenzar cada nuevo alienigena en la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Almacena la posicion horizontal exacta del alienigena
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Devolver verdadero si el alien esta en el borde de la pantalla"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """Mueve el alien a la derecha o izquierda"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        


