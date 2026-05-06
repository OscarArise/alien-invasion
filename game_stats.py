class GameStats:
    """Estadisticas de seguimiento de alien invasion"""
    def __init__(self, ai_game):
        """Inicializar estadisticas"""
        self.settings = ai_game.settings
        self.game_active = True
        self.reset_stats()
        
    def reset_stats(self):
        """Inicializar estadisticas que pueden cambiar durante el juego"""
        self.ships_left = self.settings.ship_limit        