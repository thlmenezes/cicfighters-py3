import os
import pygame
import Sprite


class GameMenu(object):
    """Menu de escolha de personagens"""

    def __init__(self, jogadores=None):
        if jogadores is None:
            jogadores = ["", "",
                [
                    pygame.K_w,
                    pygame.K_s,
                    pygame.K_a,
                    pygame.K_d,
                    pygame.K_y,
                    pygame.K_u,
                    pygame.K_i
                ], [
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    # NOTE: KP means keypad,
                    # changed for testing in more keyboard layouts
                    pygame.K_7,  # pygame.K_KP7,
                    pygame.K_8,  # pygame.K_KP8,
                    pygame.K_9   # pygame.K_KP9
                ]
            ]
        self.inicializa(jogadores)

    def inicializa(self, jogadores):
        """Inicializa elementos do menu"""
        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height()
        pygame.mixer.Sound(os.path.join('.','assets', 'Sons', "entradamenu.wav")).play()
        pygame.mixer.music.load(os.path.join('.','assets', 'Musicas', 'menu.mp3'))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        self.font = pygame.font.Font(os.path.join('.','assets', 'Imagens', "fonte.ttf"),
                                     int(self.height*0.08))
        retratos = []
        linha = []
        pos = [self.width*0.2375, self.height*0.45]
        self.postitulo = [self.width*0.32, self.height*0.34]
        self.cor = 120
        self.incrcor = 3
        self.configcontrole = 0
        # define posicoes dos retratos na tela
        for i in [string for string in
                  os.listdir(os.path.join('.','assets', 'Personagens'))
                  if not string.startswith(".")]:
            x = pos[0]
            y = pos[1]
            linha.append(Retrato(i, (x, y)))
            pos[0] = pos[0] + 120
            if (pos[0]+90) >= self.width:
                pos[1] = pos[1] + 160
                pos[0] = self.width*0.2375
                retratos.append(linha[:])
                linha = []
                # se o numero de personagens ultrapassa
                # o limite de tamanho da tela para de ler
                if (pos[1] + 120) >= self.height:
                    break
        if len(linha) > 0:
            retratos.append(linha[:])
        self.retratos = retratos
        self.retratos[0][0].seleciona(1)
        self.retratos[0][0].seleciona(2)
        self.selecionadop1 = [0, 0]
        self.selecionadop2 = [0, 0]
        self.numcolunas = int((self.width-50)/120)
        self.fundo = Sprite.Sprite(os.path.join('.','assets', 'Imagens', 'menu.png'),
                                   (0,0), 0, (self.width, self.height))
        self.botoesp1 = jogadores[2]
        self.botoesp2 = jogadores[3]
    #eventos de input
    def input(self,eventos):
        """ Trata eventos de input """
        for event in eventos:
            #Botao de fechar
            if event.type == pygame.QUIT:
                return True
            #Eventos de teclado
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    return True
                elif (event.key == pygame.K_F11):
                    pygame.display.toggle_fullscreen()
                #Controles do P1                    
                elif (event.key == self.botoesp1[3]):
                    if not self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].escolhidop1:
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].deseleciona(1)
                        self.selecionadop1[0] =  (self.selecionadop1[0] + 1) % len(self.retratos[self.selecionadop1[1]])
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].seleciona(1)
                elif (event.key == self.botoesp1[2]):
                    if not self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].escolhidop1:
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].deseleciona(1)
                        self.selecionadop1[0] =  (self.selecionadop1[0] - 1) % len(self.retratos[self.selecionadop1[1]])
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].seleciona(1)
                elif (event.key == self.botoesp1[1]):
                    if not self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].escolhidop1:
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].deseleciona(1)
                        self.selecionadop1[1] =  (self.selecionadop1[1] + 1) % len(self.retratos)
                        if len(self.retratos[self.selecionadop1[1]]) <= self.selecionadop1[0]:
                            self.selecionadop1[0] = len(self.retratos[self.selecionadop1[1]]) - 1
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].seleciona(1)
                elif (event.key == self.botoesp1[0]):
                    if not self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].escolhidop1:
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].deseleciona(1)
                        self.selecionadop1[1] =  (self.selecionadop1[1] - 1) % len(self.retratos)
                        if len(self.retratos[self.selecionadop1[1]]) <= self.selecionadop1[0]:
                            self.selecionadop1[0] = len(self.retratos[self.selecionadop1[1]]) - 1
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].seleciona(1)
                elif (event.key == self.botoesp1[4]):
                    if not self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].escolhidop1:
                        self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].escolhe(1)
                elif (event.key == self.botoesp1[5]):
                    self.retratos[self.selecionadop1[1]][self.selecionadop1[0]].desescolhe(1)
                # Controles do P2
                elif (event.key == self.botoesp2[3]):
                    if not self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].escolhidop2:
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].deseleciona(2)
                        self.selecionadop2[0] =  (self.selecionadop2[0] + 1) % len(self.retratos[self.selecionadop2[1]])
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].seleciona(2)
                elif (event.key == self.botoesp2[2]):
                    if not self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].escolhidop2:
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].deseleciona(2)
                        self.selecionadop2[0] =  (self.selecionadop2[0] - 1) % len(self.retratos[self.selecionadop2[1]])
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].seleciona(2)
                elif (event.key == self.botoesp2[1]):
                    if not self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].escolhidop2:
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].deseleciona(2)
                        self.selecionadop2[1] =  (self.selecionadop2[1] + 1) % len(self.retratos)
                        if len(self.retratos[self.selecionadop2[1]]) <= self.selecionadop2[0]:
                            self.selecionadop2[0] = len(self.retratos[self.selecionadop2[1]]) - 1
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].seleciona(2)
                elif (event.key == self.botoesp2[0]):
                    if not self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].escolhidop2:
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].deseleciona(2)
                        self.selecionadop2[1] =  (self.selecionadop2[1] - 1) % len(self.retratos)
                        if len(self.retratos[self.selecionadop2[1]]) <= self.selecionadop2[0]:
                            self.selecionadop2[0] = len(self.retratos[self.selecionadop2[1]]) - 1
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].seleciona(2)
                elif (event.key == self.botoesp2[4]):
                    if not self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].escolhidop2:
                        self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].escolhe(2)
                elif (event.key == self.botoesp2[5]):
                    self.retratos[self.selecionadop2[1]][self.selecionadop2[0]].desescolhe(2)

                elif (event.key == pygame.K_F1) and (self.configcontrole == 0):
                    self.configcontrole=1
                    self.botoesp1 = []
                elif (event.key == pygame.K_F2) and (self.configcontrole == 0):
                    self.configcontrole=2
                    self.botoesp2 = []

        return False

    def update(self, dtempo, eventos):
        """Atualiza elementos do menu"""
        self.cor = self.cor + self.incrcor
        if self.cor >= 255:
            self.incrcor = -3
            self.cor = 255
        if self.cor <= 100:
            self.incrcor = 3
        # caso um jogador esteja configurando os controles
        if self.configcontrole == 1:
            for event in eventos:
                if (event.type == pygame.KEYDOWN):
                    self.botoesp1.append(event.key)
                if len(self.botoesp1) >= 7:
                    self.botoesp1 = self.botoesp1[:7]
                    self.configcontrole = 0
            return False
        elif self.configcontrole == 2:
            for event in eventos:
                if (event.type == pygame.KEYDOWN):
                    self.botoesp2.append(event.key)
                if len(self.botoesp2) >= 7:
                    self.botoesp2 = self.botoesp2[:7]
                    self.configcontrole = 0
            return False
        else:
            self.fundo.update(dtempo)
            for i in self.retratos:
                for n in i:
                    n.update(dtempo)
            # Se os 2 jogadores ja escolheram
            selectp1Y = self.selecionadop1[1]
            selectp1X = self.selecionadop1[0]
            retratop1 = self.retratos[selectp1Y][selectp1X]

            selectp2Y = self.selecionadop2[1]
            selectp2X = self.selecionadop2[0]
            retratop2 = self.retratos[selectp2Y][selectp2X]
            if retratop1.escolhidop1 and retratop2.escolhidop2:
                return [
                    retratop1.nome,
                    retratop2.nome,
                    self.botoesp1,
                    self.botoesp2
                ]
            else:
                return self.input(eventos)

    def render(self,screen):
        """Renderiza os elementos da tela atual"""
        self.fundo.render(screen,(0,0))
        screen.blit(self.font.render("Faça Sua Matrícula", True, (self.cor,0,0)),(self.postitulo[0],self.postitulo[1]))
        for i in self.retratos:
            for n in i:
                n.render(screen)

        if self.configcontrole:
            superficieescura = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            superficieescura.fill((0,0,0,210))
            screen.blit(superficieescura,(0,0))
            screen.blit(self.font.render("Configurando Controles:", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Configurando Controles:")[0]/2),self.height*0.1))
            screen.blit(self.font.render("Pressione:", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Pressione:")[0]/2),self.height*0.4))
            listabotoes = [] 
            if self.configcontrole == 1:
                screen.blit(self.font.render("Jogador 1", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Jogador 1")[0]/2),self.height*0.2))
                listabotoes = self.botoesp1
            elif self.configcontrole == 2:
                screen.blit(self.font.render("Jogador 2", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Jogador 2")[0]/2),self.height*0.2))
                listabotoes = self.botoesp2

            if len(listabotoes) == 0: screen.blit(self.font.render("Cima", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Cima")[0]/2),self.height*0.5))
            elif len(listabotoes) == 1: screen.blit(self.font.render("Baixo", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Baixo")[0]/2),self.height*0.5))
            elif len(listabotoes) == 2: screen.blit(self.font.render("Esquerda", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Esquerda")[0]/2),self.height*0.5))
            elif len(listabotoes) == 3: screen.blit(self.font.render("Direita", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Direita")[0]/2),self.height*0.5))
            elif len(listabotoes) == 4: screen.blit(self.font.render("Soco", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Soco")[0]/2),self.height*0.5))
            elif len(listabotoes) == 5: screen.blit(self.font.render("Chute", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Chute")[0]/2),self.height*0.5))
            elif len(listabotoes) == 6: screen.blit(self.font.render("Especial", True, (self.cor,0,0)),((self.width/2)-(self.font.size("Especial")[0]/2),self.height*0.5))                
            

    def unload(self,):
        """Descarrega tela"""
        pygame.mixer.music.stop()
        pygame.time.delay(1500)
        pygame.mixer.stop()
        return True

class Retrato(object):
    """ Retrato de personagem na tela de selecao """
    def __init__(self,nome,coords):
        x,y = coords
        self.sprite = Sprite.Sprite(os.path.join('.','assets','Personagens',nome,'retrato.png'),(90,120),1.5)
        self.x = x
        self.y = y
        self.nome = nome
        self.font = pygame.font.Font(os.path.join('.','assets','Imagens',"fonte.ttf"), 20)
        self.selecionadop1 = False
        self.selecionadop2 = False
        self.escolhidop1 = False
        self.escolhidop2 = False
        self.cor = 155
        self.incrcor = 5
        self.somseleciona = pygame.mixer.Sound(os.path.join('.','assets','Sons',"seleciona.wav"))
        self.somescolhejogador = pygame.mixer.Sound(os.path.join('.','assets',"Personagens",self.nome,"escolhe.wav"))
        self.somescolhe = pygame.mixer.Sound(os.path.join('.','assets',"Sons","escolhe.wav"))

    def update(self,dtempo):
        """ Atualiza retrato e caixa de selecao """
        self.sprite.update(dtempo)
        self.cor = self.cor + self.incrcor
        if self.cor >= 255:
            self.incrcor = -5
            self.cor = 255
        if self.cor <= 155: self.incrcor = 5

    def render(self,screen):
        """ Renderiza retrato e caixa de selecao """
        self.sprite.render(screen,(self.x,self.y))
        screen.blit(self.font.render(self.nome, True, (155,0,0)),(self.x+45-(self.font.size(self.nome)[0]/2),self.y + 130))
        if (not self.escolhidop1) and (not self.escolhidop2):
            if self.selecionadop1:
                pygame.draw.rect(screen, (self.cor,0,0), pygame.Rect(self.x-5,self.y-5,95,125), 5)
            if self.selecionadop2:
                pygame.draw.rect(screen, (0,0,self.cor), pygame.Rect(self.x-5,self.y-5,95,125), 5)
        elif self.escolhidop1:
            pygame.draw.rect(screen, (255,20,0), pygame.Rect(self.x-5,self.y-5,95,125), 5)
        elif self.escolhidop2:
            pygame.draw.rect(screen, (0,20,255), pygame.Rect(self.x-5,self.y-5,95,125), 5)

    def seleciona(self,player):
        """ define o jogador de determinado numero como seletor do retrato """
        if player == 1: self.selecionadop1 = True
        else: self.selecionadop2 = True

    def deseleciona(self,player):
        """ desmarca o jogador de determinado numero como seletor do retrato """
        if player == 1: self.selecionadop1 = False
        else: self.selecionadop2 = False
        self.somseleciona.play()

    def escolhe(self,player):
        """ define o jogador de determinado numero como seletor do retrato """
        if player == 1: self.escolhidop1 = True
        else: self.escolhidop2 = True
        self.somescolhe.play()
        self.somescolhejogador.play()

    def desescolhe(self,player):
        """ desmarca o jogador de determinado numero como seletor do retrato """
        if player == 1: self.escolhidop1 = False
        else: self.escolhidop2 = False

