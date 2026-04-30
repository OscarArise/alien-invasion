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
        
        #Bandera de movimiento izquierda derecha
        self.moving_right = False
        self.moving_left = False
        
        #Bandera de movimiento arriba y abajo
        self.moving_up = False
        self.moving_down = False
        
    def update_moving(self):
        """Actualiza la posicion del barco segun la bandera de movimiento"""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1
        if self.moving_up:
            self.rect.y -= 1
        if self.moving_down:
            self.rect.y += 1
    
    def blitme(self):
        """Dibuja el barco en su ubicacion actual"""
        self.screen.blit(self.image,self.rect)