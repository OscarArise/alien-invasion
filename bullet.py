import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Una clase para manejar las balas disparadas de la nave"""
    def __init__(self, ai_game):
        """Crea un objeto de bala en la posicion actual de la nave"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        #Cree un rectangulo de bala en (0,0) y luego establezca la posicion correcta
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #Almacena la posicion de la vineta como un valor decimal
        self.y = float(self.rect.y)
        
    def update(self):
        """Mueve la bala hacia la posicion de arriba en la pantalla"""
        #Actualizar la posicion decimal de la vineta
        self.y -= self.settings.bullet_speed
        #Actualizar la posicionde rect
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Dibuja la vineta hacia la pantalla"""
        pygame.draw.rect(self.screen,self.color,self.rect)