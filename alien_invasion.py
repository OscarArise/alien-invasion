import sys
import pygame
from settings import Settings

class Alien_invasion:
    """Clase general para administrar los activos y el comportamiento del juego"""
    def __init__(self):
        """Inicializa el juego y crea recursos del juego"""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
    def run_game(self):
        """Iniciar el bucle principal del juego"""
        while True:
            #Este antento a los eventos del mouse y teclado
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
            #Vuelva a dibujar la pantalla durante cada pasa del bucle
            self.screen.fill(self.settings.bg_color)
                    
            #Hacer visible la pantalla dibujada mas reciente
            pygame.display.flip()
            
if __name__ == '__main__':
    #Cree una instancia de juego y ejecute el juego
    ai = Alien_invasion()
    ai.run_game()
            