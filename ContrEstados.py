import pygame
import GameMenu
import Ringue
import VersusScreen
import Tutorial


class ContrEstados(object):
    """Controladora de estados, telas"""

    def __init__(self,):
        self.inicializa()

    def inicializa(self,):
        """Inicia engine de jogo"""
        self.Tela = Tutorial.Tutorial()
        self.retorno = False

    def update(self, dtempo, eventos):
        """Atualiza elementos do estado atual"""

        self.retorno = self.Tela.update(dtempo, eventos)  
        if self.retorno == pygame.QUIT:
            return True 
        elif not self.retorno:
            return False
        else:
            # Retorna algo quando a partida acaba
            # ou quando o jogador sai do menu
            if isinstance(self.Tela, Tutorial.Tutorial):
                self.Tela.unload()
                self.Tela = GameMenu.GameMenu()
            elif isinstance(self.Tela, VersusScreen.VersusScreen):
                self.Tela.unload()
                self.Tela = Ringue.Ringue(self.retorno)
            elif isinstance(self.Tela, GameMenu.GameMenu):
                self.Tela.unload()
                self.Tela = VersusScreen.VersusScreen(self.retorno)
            elif isinstance(self.Tela, Ringue.Ringue):
                self.Tela.unload()
                self.Tela = GameMenu.GameMenu(self.retorno)
        return False

    def render(self, screen):
        """Renderiza os elementos da tela atual"""
        self.Tela.render(screen)
        pygame.display.flip()

    def unload(self,):
        """Descarrega Controladora"""
        return True
