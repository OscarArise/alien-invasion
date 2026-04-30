import pygame

class Ship: 
    """Una clase para manejar la nave"""
    def __init__(self,ai_game):
        """Inicializar la nave y establecer su posicion inicial"""
        #Apunta a la pantalla
        self.screen = ai_game.screen
        #Apunta a los ajustes
        self.settings = ai_game.settings
        
        self.screen_rect = ai_game.screen.get_rect()
        
        #Cargue la imagen del barco y obtenga su rect
        self.image = pygame.image.load('images/DurrrSpaceShip.png').convert_alpha()
        self.imagerect = self.image.get_rect()
        
        #Comience cada nueva nave en la parte inferior de la pantalla
        self.imagerect.midbottom = self.screen_rect.midbottom
        
        #Almacena un valor decimal para la posiciion horizontal de la nave
        self.x = float(self.imagerect.x)
        self.y = float(self.imagerect.y)

        #Bandera de movimiento izquierda derecha
        self.moving_right = False
        self.moving_left = False
        
        #Bandera de movimiento arriba y abajo
        self.moving_up = False
        self.moving_down = False
        
    def update_moving(self):
        """Actualiza la posicion del barco segun la bandera de movimiento"""
        if self.moving_right and self.imagerect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.imagerect.left > 0:
            self.x -= self.settings.ship_speed
            
        if self.moving_up and self.imagerect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.imagerect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        #Actualizar el objeto rect de self.x
        self.imagerect.x = self.x    
        self.imagerect.y = self.y
        
    
    def blitme(self):
        """Dibuja el barco en su ubicacion actual"""
        self.screen.blit(self.image,self.imagerect)