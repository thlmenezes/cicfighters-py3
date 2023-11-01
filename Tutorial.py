import os
import pygame
import Sprite

class Tutorial(object):
    """Tutorial"""

    def __init__(self, jogadores=None):
        """Inicializa elementos do menu"""
        width = pygame.display.get_surface().get_width()
        height = pygame.display.get_surface().get_height()
        self.fundo = Sprite.Sprite(os.path.join('.', 'assets', 'Imagens', 'tutorialimage.png'),
                                   (0, 0), 0, (width, height))

    # eventos de input
    def input(self, eventos):
        """ Trata eventos de input """
        for event in eventos:
            # Botao de fechar
            if event.type == pygame.QUIT:
                return pygame.QUIT
            # Eventos de teclado
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    return pygame.QUIT
                elif (event.key == pygame.K_F11):
                    pygame.display.toggle_fullscreen()
                else:
                    return "MENU"
        return False

    def update(self, dtempo, eventos):
        """Atualiza elementos do menu"""
        return self.input(eventos)

    def render(self, screen):
        """Renderiza os elementos da tela atual"""
        self.fundo.render(screen, (0, 0))

    def unload(self, ):
        """Descarrega tela"""
        return True