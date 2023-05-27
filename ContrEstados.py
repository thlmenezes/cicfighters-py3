import pygame

import GameMenu
# from Ringue import *
# from VersusScreen import *


class ContrEstados(object):
    """Controladora de estados, telas"""

    def __init__(self,):
        self.inicializa()

    def inicializa(self,):
        """Inicia engine de jogo"""
        self.Tela = GameMenu.GameMenu()
        self.retorno = False

    def update(self, dtempo, eventos):
        """Atualiza elementos do estado atual"""

        self.retorno = self.Tela.update(dtempo, eventos)
        if self.retorno:
            # Retorna algo quando a partida acaba
            # ou quando o jogador sai do menu
            if self.Tela.__class__ == GameMenu:
                if self.retorno:
                    return True
                else:
                    self.Tela.unload()
                    # self.Tela = VersusScreen(self.retorno)
            # elif self.Tela.__class__ == Ringue:
            #     self.Tela.unload()
            #     self.Tela = GameMenu.GameMenu(self.retorno)
            # elif self.Tela.__class__ == VersusScreen:
            #     self.Tela.unload()
            #     self.Tela = Ringue(self.retorno)

        return False

    def render(self, screen):
        """Renderiza os elementos da tela atual"""
        self.Tela.render(screen)
        pygame.display.flip()

    def unload(self,):
        """Descarrega Controladora"""
        return True
