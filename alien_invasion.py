import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from buttom import Button
from scoreboard import Scoreboard

class Alien_invasion:
    """Clase general para administrar los activos y el comportamiento del juego"""
    def __init__(self):
        """Inicializa el juego y crea recursos del juego"""
        pygame.init()
        #instancia de settings
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        #Crea una instancia para almacenar estadisticas del juego
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)        # <-- ¿tienes esta línea?

        
        #instancia de Ship
        self.ship = Ship(self)
    
        #Bullets
        self.bullets = pygame.sprite.Group()
        
        #Instancia de Alien
        self.aliens = pygame.sprite.Group()
                
        self._create_fleet()
        
        #Estado de pausa
        self.game_paused = False
        
        #Botones
        self.play_button = Button(self, "Play")
        self.resume_button = Button(self, "Resume", y_offset=-40)
        self.quit_button = Button(self, "Quit (Q)", y_offset=40)
        
        # Fuente para overlays (pausa / game over)
        self.overlay_font_big = pygame.font.SysFont(None, 80)
        self.overlay_font_small = pygame.font.SysFont(None, 40)

        # Reloj para estabilizar FPS
        self.clock = pygame.time.Clock()
        
        
            
    def run_game(self):
        """Iniciar el bucle principal del juego"""
        while True:
            #Revisa los eventos del mouse y teclado
            self.check_events()
            
            if self.stats.game_active and not self.game_paused:

                #Actualizar el movimiento de la nave
                self.ship.update_moving()
                
                #Actualiza las balas
                self.update_bullets()
                
                #Actualiza el moviemiento del los aliens
                self.update_aliens()
            
            #Actualizacion de los objetos en pantalla
            self.update_screen() 
            self.clock.tick(6000)
            
    def check_events(self):
         for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    self.check_keydown_events(event)
                
                elif event.type == pygame.KEYUP:
                    self.check_keyup_events(event)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_button_clicks(mouse_pos)
                
    
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
        elif event.key == pygame.K_p:
            #p Arranca el juego desde la pantalla de inicio
            if not self.stats.game_active:
                self._start_game()
            #P tambien pausa y reanuda
            elif self.stats.game_active:
                self._toggle_pause()
            
    def check_keyup_events(self,event):
         if event.key == pygame.K_RIGHT:
             self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:
             self.ship.moving_left = False
         elif event.key == pygame.K_UP:
             self.ship.moving_up = False
         elif event.key == pygame.K_DOWN:
             self.ship.moving_down = False
             
    def _check_button_clicks(self, mouse_pos):
        """Detecta clics en los botones según el estado del juego"""
        if not self.stats.game_active:
            # Pantalla de inicio: botón Play
            if self.play_button.rect.collidepoint(mouse_pos):
                self._start_game()
        elif self.game_paused:
            # Pantalla de pausa: Resume o Quit
            if self.resume_button.rect.collidepoint(mouse_pos):
                self._toggle_pause()
            elif self.quit_button.rect.collidepoint(mouse_pos):
                sys.exit()
    def _start_game(self):
        """Reinicia el juego y lo activa"""
        self.settings.__init__()          # Restaura velocidades originales
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.game_has_started = True  # marca que ya jugó
        self.game_paused = False

        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()

        # Actualiza el HUD con los valores reiniciados
        self.sb.prep_score()
        self.sb.prep_high_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        pygame.mouse.set_visible(False)
    
    def _toggle_pause(self):
        """Alterna entre pausado y activo"""
        self.game_paused = not self.game_paused
        pygame.mouse.set_visible(self.game_paused)

    
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
                
        self.check_bullet_alien_collisions()
        
        
    def check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            # Suma puntos por cada alien eliminado en la colisión
            for aliens_hit in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens_hit)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Sube de nivel al limpiar la pantalla
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
                
                
    def update_aliens(self):
        """Comprueba si la flota esta en un borde.
        Luego actualice las posiciones de todos los aliens en la flota"""
        self.check_fleet_edges()
        self.aliens.update()
        
        #Busque colisiones de naves alienigenas
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()
        
        #Busca aliens que han golpeado la parte inferior de la pantalla
        self.check_aliens_bottom()
                
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
        
    def check_fleet_edges(self):
        """Responda adecuadamente si algun alien ha llegado al borde"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break
    
    def change_fleet_direction(self):
        """Deja caer toda la flota y cambia la direccion de la flota"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def ship_hit(self):
        """Responder a la nave siendo golpeada por un alien"""
        #Decrementar naves a la izquierda
        self.stats.ships_left -= 1
        self.sb.prep_ships()
        
        if self.stats.ships_left > 0:
            #Deshazte de los aliens y balas restantes
            self.aliens.empty()
            self.bullets.empty()
            #Crea una nueva flota 
            self._create_fleet()
            self.ship.center_ship()
            #Pausa
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    
    def check_aliens_bottom(self):
        """Comprueba si algun alien ha llegado al final de la pantalla"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Tratar de la misma forma como si la nave hubiera sido golpeada
                self.ship_hit()
                break
    
    def _draw_overlay(self, alpha=160):
        """Dibuja un rectángulo semitransparente sobre el juego"""
        overlay = pygame.Surface(
            (self.settings.screen_width, self.settings.screen_height),
            pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        self.screen.blit(overlay, (0, 0))

    def _draw_start_screen(self):
        """Pantalla de inicio: título + botón Play"""
        self._draw_overlay()
        title = self.overlay_font_big.render(
            "ALIEN INVASION", True, (255, 255, 255))
        title_rect = title.get_rect()
        title_rect.centerx = self.screen.get_rect().centerx
        title_rect.centery = self.screen.get_rect().centery - 80
        self.screen.blit(title, title_rect)
        self.play_button.draw_button()

        hint = self.overlay_font_small.render(
            "Presiona P o haz clic en Play", True, (200, 200, 200))
        hint_rect = hint.get_rect()
        hint_rect.centerx = self.screen.get_rect().centerx
        hint_rect.top = self.play_button.rect.bottom + 20
        self.screen.blit(hint, hint_rect)

    def _draw_pause_screen(self):
        """Pantalla de pausa: cartel + botones Resume/Quit"""
        self._draw_overlay()
        paused_text = self.overlay_font_big.render(
            "PAUSADO", True, (255, 255, 100))
        paused_rect = paused_text.get_rect()
        paused_rect.centerx = self.screen.get_rect().centerx
        paused_rect.centery = self.screen.get_rect().centery - 100
        self.screen.blit(paused_text, paused_rect)
        self.resume_button.draw_button()
        self.quit_button.draw_button()

    def _draw_game_over_screen(self):
        """Pantalla de Game Over: mensaje + puntaje final + instrucciones"""
        self._draw_overlay()
        screen_rect = self.screen.get_rect()

        go_text = self.overlay_font_big.render(
            "GAME OVER", True, (220, 50, 50))
        go_rect = go_text.get_rect(centerx=screen_rect.centerx,
                                   centery=screen_rect.centery - 80)
        self.screen.blit(go_text, go_rect)

        score_text = self.overlay_font_small.render(
            f"Puntaje: {self.stats.score:,}   Mejor: {self.stats.high_score:,}",
            True, (255, 255, 255))
        score_rect = score_text.get_rect(centerx=screen_rect.centerx,
                                         centery=screen_rect.centery)
        self.screen.blit(score_text, score_rect)

        restart_text = self.overlay_font_small.render(
            "Presiona P para volver a jugar  |  Q para salir",
            True, (180, 180, 180))
        restart_rect = restart_text.get_rect(centerx=screen_rect.centerx,
                                              centery=screen_rect.centery + 60)
        self.screen.blit(restart_text, restart_rect)
    
    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # HUD siempre visible durante el juego
        if self.stats.game_active or self.game_paused:
            self.sb.show_score()

        # Overlays según el estado
        if not self.stats.game_active:
            if not self.stats.game_has_started:
                self._draw_start_screen()
            else:
                self._draw_game_over_screen()
                
        elif self.game_paused:
            self._draw_pause_screen()

        pygame.display.flip()
        
        
            
if __name__ == '__main__':
    #Cree una instancia de juego y ejecute el juego
    ai = Alien_invasion()
    ai.run_game()
            