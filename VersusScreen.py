import os
import sys
import pygame
from pygame.locals import *

from Sprite import *


class VersusScreen():
    """Classe da tela de versus"""

    def __init__(self, jogadores):
        """Inicia tela de versus"""
        # Inicia alguns verificadores usados posteriormente na cena
        self.jogadores = jogadores
        self.teclas = [pygame.K_F11] + jogadores[2][4:7] + jogadores[3][4:7]
        self.tela = pygame.display.get_surface()
        self.area = self.tela.get_rect()
        self.width = self.tela.get_width()
        self.height = self.tela.get_height()
        self.deslocax = 0.
        self.parou = False
        self.primeiraiteracao = True



        # Carrega fundo da tela de versus
        self.fundo = Sprite(os.path.join(
            '.', 'assets', 'Imagens', "vsback.png"), (0, 0), False, (self.width, self.height))

        # Carrega personagem player 1
        self.player1 = Sprite(os.path.join('.', 'assets', 'Personagens', self.jogadores[0], "vs.png"), (
            0, 0), False, (self.width*0.5, self.height*0.598333333))

        # Carrega personagem player 2
        self.player2 = Sprite(os.path.join('.', 'assets', 'Personagens', self.jogadores[1], "vs.png"), (
            0, 0), False, (self.width*0.5, self.height*0.598333333))

    def update(self, dtempo, eventos):
        """Atualiza a tela de versus"""
        # descarta primeiro dtempo (tempo para carregar tela)
        if self.primeiraiteracao:
            self.primeiraiteracao = False
            dtempo = 0
            # Som de introducao da tela de versus
            pygame.mixer.Sound(os.path.join(
                '.', 'assets', 'Sons', "vs.wav")).play()

        # Cuida da animacao da tela de versus
        if not self.parou:
            self.deslocax = self.deslocax + (self.width*0.25)*dtempo
            if ((self.deslocax - (self.player1.frames[0].get_width()*0.75)) >= (self.area.centerx - 5 - self.player1.frames[0].get_width())):
                self.deslocax = (self.player1.frames[0].get_width(
                )*0.75) + (self.area.centerx - 5 - self.player1.frames[0].get_width())
                self.parou = True

        if self.parou == True:
            return self.jogadores
        return False

    def render(self, tela):
        """Renderiza a tela e mostra ela"""
        self.fundo.render(tela, (0, 0))
        self.player1.render(
            tela, (-(self.player1.frames[0].get_width()*0.75), (self.height * 0.41)), (self.deslocax, 0), False)
        self.player2.render(tela, ((self.player2.frames[0].get_width(
        )*1.75), (self.height * 0.41)), (-self.deslocax, 0), True)

    def unload(self,):
        pygame.mixer.stop()
        return True
