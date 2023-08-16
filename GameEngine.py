import pygame
import time

import ContrEstados


class GameEngine(object):
    """Engine de jogo principal"""

    def __init__(self, fullscreen):
        self.fullscreen = fullscreen
        self.inicializa()

    def inicializa(self,):
        """Inicia engine de jogo"""
        # Inicializa pygame
        pygame.init()

        # Inicializa tempo
        self.tempoantigo = time.time()

        if self.fullscreen:
            self.window = pygame.display.set_mode((800, 600),
                                                  pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((800, 600))

        pygame.mouse.set_visible(False)
        self.screen = pygame.display.get_surface()

        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()

    def run(self,):
        """Loop principal do jogo, calcula tempo e\
executa controlador de estados"""
        Estado = ContrEstados.ContrEstados()

        sair = False
        # Captura tempo
        while not sair:
            # seta dtempo
            tempo = time.time()
            dtempo = tempo - self.tempoantigo
            self.tempoantigo = tempo

            sair = Estado.update(dtempo, pygame.event.get())
            Estado.render(self.screen)

        Estado.unload()
        pygame.quit()
        return True
