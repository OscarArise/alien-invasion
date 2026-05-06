import pygame.font

class Scoreboard:
    """Muestra la información de puntuación en pantalla"""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 40)

        # Prepara todas las imágenes de texto al inicio
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Renderiza la puntuación actual (esquina superior derecha)"""
        score_str = f"Score: {self.stats.score:,}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        """Renderiza el puntaje máximo (parte superior central)"""
        hs_str = f"Best: {self.stats.high_score:,}"
        self.high_score_image = self.font.render(hs_str, True,
                                                 self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 10

    def prep_level(self):
        """Renderiza el nivel actual (debajo de la puntuación)"""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 5

    def prep_ships(self):
        """Renderiza las vidas restantes como texto (esquina superior izquierda)"""
        ships_str = f"Vidas: {self.stats.ships_left}"
        self.ships_image = self.font.render(ships_str, True,
                                            self.text_color, self.settings.bg_color)
        self.ships_rect = self.ships_image.get_rect()
        self.ships_rect.left = 20
        self.ships_rect.top = 10

    def check_high_score(self):
        """Actualiza el puntaje máximo si se supera"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Dibuja todo el HUD en pantalla"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.ships_image, self.ships_rect)