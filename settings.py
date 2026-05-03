class Settings:
    """Una clase para almacenar todos los ajustes de alien invasion"""
    def __init__(self):
        """Inicializa la configuracion del juego"""
        #Ajuste de la pantalla
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (10, 25, 60)
        self.ship_speed = 1.5
        #configuracion de las ballas
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.limit_bullets = 3
        #Configuracion alienigena
        self.alien_speed = 0.2
        self.fleet_drop_speed = 5
        #Fleet_direction de 1 representa la derecha; -1 representa la izquierda
        self.fleet_direction = 1