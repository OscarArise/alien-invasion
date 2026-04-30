import pygame

class Ship: 
    """Una clase para manejar la nave"""
    def __init__(self,ai_game):
        """Inicializar la nave y establecer su posicion inicial"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        #Cargue la imagen del barco y obtenga su rect
        self.image = pygame.image.load('images/DurrrSpaceShip.png').convert_alpha()
        self.rect = self.image.get_rect()
        
        #Comience cada nueva nave en la parte inferior de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom
        
    def blitme(self):
        """Dibuja el barco en su ubicacion actual"""
        self.screen.blit(self.image,self.rect)