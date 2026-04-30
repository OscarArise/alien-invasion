import sys
import pygame
from settings import Settings
from ship import Ship
from enemyShip import Enemy_ship

class Alien_invasion:
    """Clase general para administrar los activos y el comportamiento del juego"""
    def __init__(self):
        """Inicializa el juego y crea recursos del juego"""
        pygame.init()
        #instancia de settings
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        #instancia de Ship
        self.ship = Ship(self)
        #instancia de enemy
        self.enemy = Enemy_ship(self)

        
    def run_game(self):
        """Iniciar el bucle principal del juego"""
        while True:
            #Revisa los eventos del mouse y teclado
            self.check_events()
            
            #Actualizar el movimiento de la nave
            self.ship.update_moving()
            
            #Actualizacion de los objetos en pantalla
            self.update_screen() 
            
    def check_events(self):
         for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        #Mueve la nave a la derecha
                        self.ship.moving_right = True
                    elif event.key == pygame.K_LEFT:
                        #Mueve la nave a la izquierda
                        self.ship.moving_left = True
                        #Mueve la nave hacia arriba
                    elif event.key == pygame.K_UP:
                        self.ship.moving_up = True
                        #mueve la nave hacia abajo
                    elif event.key == pygame.K_DOWN:
                        self.ship.moving_down = True
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False
                    elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = False
                    elif event.key == pygame.K_UP:
                        self.ship.moving_up = False
                    elif event.key == pygame.K_DOWN:
                        self.ship.moving_down = False
                    
    def update_screen(self):
        #Vuelva a dibujar la pantalla durante cada pasa del bucle
        self.screen.fill(self.settings.bg_color)
        #Dibuja la nave en cada actualizacion del bucle
        self.ship.blitme()
        #Dibuja la nave enemiga
        self.enemy.enemyblitme()
        #Actualizar cada pantalla a la version mas reciente
        pygame.display.flip()
        
        
            
if __name__ == '__main__':
    #Cree una instancia de juego y ejecute el juego
    ai = Alien_invasion()
    ai.run_game()
            