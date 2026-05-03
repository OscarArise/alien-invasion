import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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
    
        #Bullets
        self.bullets = pygame.sprite.Group()
        
        #Instancia de Alien
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
            
    def run_game(self):
        """Iniciar el bucle principal del juego"""
        while True:
            #Revisa los eventos del mouse y teclado
            self.check_events()
            
            #Actualizar el movimiento de la nave
            self.ship.update_moving()
            
            #Actualiza las balas
            self.update_bullets()
            
            #Actualizacion de los objetos en pantalla
            self.update_screen() 
            
    def check_events(self):
         for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    self.check_keydown_events(event)
                
                elif event.type == pygame.KEYUP:
                    self.check_keyup_events(event)
                
    
    def check_keydown_events(self,event):
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
            #Salir con la q
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
            
    def check_keyup_events(self,event):
         if event.key == pygame.K_RIGHT:
             self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:
             self.ship.moving_left = False
         elif event.key == pygame.K_UP:
             self.ship.moving_up = False
         elif event.key == pygame.K_DOWN:
             self.ship.moving_down = False
             
    def fire_bullet(self):
        """Crea una nueva bala y la agrega al grupo de balas"""
        if len(self.bullets) < self.settings.limit_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def update_bullets(self):
        """Actualiza la posicion de las balas y deshacerce de las balas viejas"""
        self.bullets.update()
        #Deshace las balas que han desaparecido
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
                
    def _create_fleet(self):
        """Crea una flota de alienigenas"""            
        #Crea un alien y encuentra el numero de extraterrestres seguidos
        #El espacio entre cada alien es igual al ancho de un alien
        alien = Alien(self)
        alien_width, alien_heigth  = alien.rect.size
        available_space_x = self.settings.screen_width - (1 * alien_width)
        aliens_number_x = available_space_x // (2 * alien_width)
        
        #Determina la cantidad de filas alienigenas que caben en la pantalla
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_heigth ) - ship_height)
        number_rows = available_space_y // (2 * alien_heigth )
        
        #Crear la flota completa de alienigenas
        for row_number in range(number_rows):
            for alien_number in range(aliens_number_x):
                self.create_aliens(alien_number, row_number)
        
    def create_aliens(self, alien_number, row_number):
        """Crea el alien y colocalo en la fila"""
        alien = Alien(self)
        alien_width, alien_heigth  = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

        self.aliens.add(alien)
        
    
    def update_screen(self):
        #Vuelva a dibujar la pantalla durante cada pasa del bucle
        self.screen.fill(self.settings.bg_color)
        #Dibuja la nave en cada actualizacion del bucle
        self.ship.blitme()
        #Actualiza y recorre la lista de balas
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        #Dibujar a los enemigos
        self.aliens.draw(self.screen)
        
        #Actualizar cada pantalla a la version mas reciente
        pygame.display.flip()
        
        
            
if __name__ == '__main__':
    #Cree una instancia de juego y ejecute el juego
    ai = Alien_invasion()
    ai.run_game()
            