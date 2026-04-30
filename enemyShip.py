import pygame

class Enemy_ship:
    """Dibujar al enemigo"""
    def __init__(self,ei_game):
        """Iniciar el enemigo y establecer su posicion"""
        self.screen = ei_game.screen
        self.screen_rect = ei_game.screen.get_rect()
        
        #Cargando la imagen del enemigo y obtener su rectangulo
        self.enemy_image = pygame.image.load('images/fighter.png').convert_alpha()
        self.imagerect = self.enemy_image.get_rect()
        
        #Comience cada nuevo enemigo en la parte central de la pantalla
        self.imagerect.center = self.screen_rect.center
    
    def enemyblitme(self):
        """Dibuja al enemigo en su ubicacion"""
        self.screen.blit(self.enemy_image,self.imagerect)
    