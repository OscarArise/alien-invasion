import pygame.font

class Button:
    """Boton generico reusable para menu"""
    def __init__(self, ai_game, msg, y_offset=0):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        self.width, self.height = 220, 55
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.centery += y_offset
        
        self.prep_msg(msg)
        
    def prep_msg(self, msg):
        """Convierte el texto en imagen y lo centra en el boton"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
        