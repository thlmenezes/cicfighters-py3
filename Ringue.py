import os,sys
import pygame
from pygame.locals import *
from Sprite import *
import random

class Ringue(object):
    """ Classe responsavel pelo estado principal do jogo, o ringue de luta """
    def __init__(self,jogadores):
        self.inicializa(jogadores)
        
    def inicializa(self,jogadores):
        """ Inicializa elementos do ringue de luta """
        self.jogadores = jogadores
        personagens = jogadores[0:2]
        controlesp1 = jogadores[2]
        controlesp2 = jogadores[3]
        self.screenwidth = pygame.display.get_surface().get_width()
        self.screenheight = pygame.display.get_surface().get_height()
        self.nomes = personagens
        ringueescolhido = random.choice([s for s in os.listdir(os.path.join('.','Ringues','Fundo')) if not s.startswith(".")])
        self.ringue = Sprite(os.path.join('.','Ringues','Fundo',ringueescolhido),(800,600),1.5,(self.screenwidth, self.screenheight))
        self.frenteringue = False
        if ringueescolhido in [s for s in os.listdir(os.path.join('.','Ringues','Frente')) if not s.startswith(".")]:
            self.frenteringue = Sprite(os.path.join('.','Ringues','Frente',ringueescolhido),(800,600),1,(self.screenwidth, self.screenheight))
        self.musicaescolhida = random.choice([s for s in os.listdir(os.path.join('.','Musicas','Normais')) if not s.startswith(".")])
        pygame.mixer.music.load(os.path.join('.','Musicas','Normais',self.musicaescolhida))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
        self.p1 = Player(self.nomes[0],(self.screenwidth/4,self.screenheight - 380),controlesp1)
        self.p2 = Player(self.nomes[1],(((self.screenwidth/4)*3)-120,self.screenheight - 380),controlesp2)
        self.p1.adversario = self.p2
        self.p2.adversario = self.p1
        self.barrap1 = Barra(
                (self.screenwidth//16,self.screenheight//16),
                (self.screenwidth//2)-(self.screenwidth//8),
                self.screenheight//32,self.p1,
                False)
        self.barrap2 = Barra(
                ((self.screenwidth//2)+(self.screenwidth//16),self.screenheight//16),
                (self.screenwidth//2)-(self.screenwidth//8),
                self.screenheight//32,self.p2,
                False)
        self.sangues = []
        self.momentotenso = False
        self.vitoria = False
        self.chuvadebits = Chuvadebits(3000)
        self.hpinicial = self.p1.hp

    #eventos de input
    def input(self,eventos):
        """ Trata eventos de input """
        for event in eventos:
            #Botao de fechar
            if event.type == QUIT:
                return self.jogadores
            #Eventos de teclado
            elif event.type == KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    return self.jogadores
                elif (event.key == pygame.K_RETURN):
                    pygame.display.toggle_fullscreen()

        return False
        
    def update(self,dtempo,eventos):
        """ Atualiza os elementos do jogo """
        self.p1.update(dtempo,eventos)
        self.p2.update(dtempo,eventos)
        for i in self.sangues:
            i.update(dtempo)
            if i.tempo > 0.7: self.sangues.remove(i)

        if self.p1.projetil.caixacolisao and self.p2.projetil.caixacolisao:
            if self.p1.projetil.caixacolisao.colliderect(self.p2.projetil.caixacolisao):
                self.p1.projetil.caixacolisao = False
                self.p2.projetil.caixacolisao = False            
        
        a,b = self.p1,self.p2
        for i in range(2):
            if a.caixagolpe:
                if a.caixagolpe.colliderect(b.caixacorpo):
                    if (b.guardabaixa <= 0)\
                    and (((b.x >= a.x) and b.andandodireita) or ((b.x < a.x) and b.andandoesquerda))\
                    and (not b.morto):
                        a.caixagolpe = False
                        a.golpecontabilizado = True
                        b.hp = b.hp - 1
                        b.defendendo = True
                        b.cooldown = 0.1
                        a.cooldown = 0.2
                        if b.abaixado: b.animatual = b.animacoes["defesa-abaixado"]
                        else: b.animatual = b.animacoes["defesa"]
                        random.choice(b.somdefesa).play()
                    else:
                        retacerto = a.caixagolpe.clip(b.caixacorpo)
                        a.caixagolpe = False
                        a.golpecontabilizado = True
                        b.hp = b.hp - 5
                        b.apanhando = True
                        b.cooldown = 0.3
                        a.cooldown = 0.2
                        random.choice(b.somapanhando).play()
                        b.animacoes["golpeado"]
                        b.socando = False
                        b.caixagolpe = False
                        b.chutando = False
                        #gera particulas de sangue
                        for i in range(random.randint(10,50)):
                            self.sangues.append(Sangue((retacerto.centerx,retacerto.centery),self.screenheight-60,(b.x >= a.x)))
                            
            if a.projetil.caixacolisao:
                if a.projetil.caixacolisao.colliderect(b.caixacorpo):
                    if (b.guardabaixa <= 0)\
                    and (((b.x >= a.x) and b.andandodireita) or ((b.x < a.x) and b.andandoesquerda))\
                    and (not b.morto):
                        a.projetil.caixacolisao = False
                        b.defendendo = True
                        b.cooldown = 0.2
                        if b.abaixado: b.animatual = b.animacoes["defesa-abaixado"]
                        else: b.animatual = b.animacoes["defesa"]
                        random.choice(b.somdefesa).play()
                    else:
                        retacerto = a.projetil.caixacolisao.clip(b.caixacorpo)
                        a.projetil.caixacolisao = False
                        b.hp = b.hp - 3
                        b.apanhando = True
                        b.cooldown = 0.5
                        random.choice(b.somapanhando).play()
                        b.animacoes["golpeado"]
                        b.socando = False
                        b.caixagolpe = False
                        b.chutando = False
                        #gera particulas de sangue
                        for i in range(random.randint(5,25)):
                            self.sangues.append(Sangue((retacerto.centerx,retacerto.centery),self.screenheight-60,(b.x >= a.x)))
            if a.hp<=0:
                if not self.vitoria:
                    self.vitoria = Vitoria(b.nome,(b == self.p1) and 1 or 2)
                    a.caixagolpe = False
                for i in range(random.randint(0,3)):
                    self.sangues.append(Sangue((a.caixacorpo.centerx,a.caixacorpo.centery),self.screenheight-60,not a.mortonadireita))
                    

            if (a.hp <= 0.4 * self.hpinicial) and not self.momentotenso:
                self.momentotenso = True
                pygame.mixer.music.stop()
                if self.musicaescolhida in os.listdir(os.path.join('.','Musicas','Tensas')):
                    musicatensa = self.musicaescolhida
                else:
                    musicatensa = random.choice(os.listdir(os.path.join('.','Musicas','Tensas')))
                pygame.mixer.music.load(os.path.join('.','Musicas','Tensas',musicatensa))
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)
            a,b = b,a
                    
        self.ringue.update(dtempo)
        if self.frenteringue: self.frenteringue.update(dtempo)
        self.barrap1.update(dtempo)
        self.barrap2.update(dtempo)
        if self.vitoria: self.vitoria.update(dtempo)
        self.chuvadebits.update(dtempo)
        return self.input(eventos)

    def render(self,screen):
        """ Renderiza os elementos da tela """
        self.ringue.render(screen,(0,0))
        self.p1.render(screen)
        self.p2.render(screen)
        for i in self.sangues:
            i.render(screen)
        self.barrap1.render(screen)
        self.barrap2.render(screen)
        if self.frenteringue: self.frenteringue.render(screen,(0,0))
        if self.vitoria : self.vitoria.render(screen)
        self.chuvadebits.render(screen)

        return True        

    def unload(self,):
        """Descarrega tela"""
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        return True

class Player(object):
    """ Classe que define um jogador (lutador na tela) """
    def __init__(self,nome, xxx_todo_changeme,controles):
        (x,y) = xxx_todo_changeme
        self.screenwidth = pygame.display.get_surface().get_width()
        self.adversario = self
        self.nome = nome
        self.x = x
        self.y = y
        self.yinicial = y
        self.projetil = Projetil(os.path.join('.','Personagens',self.nome,'projetil.png'))
        self.animacoes = {"parado":Sprite(os.path.join('.','Personagens',self.nome,'parado.png'),(305,320),8),
                          "andando":Sprite(os.path.join('.','Personagens',self.nome,'andando.png'),(305,320),8),
                          "pulando":Sprite(os.path.join('.','Personagens',self.nome,'pulando.png'),(305,320),8),
                          "abaixado":Sprite(os.path.join('.','Personagens',self.nome,'abaixado.png'),(305,320),8),
                          "socando":Sprite(os.path.join('.','Personagens',self.nome,'socando.png'),(305,320),15),
                          "socando-abaixado":Sprite(os.path.join('.','Personagens',self.nome,'socando-abaixado.png'),(305,320),10),
                          "socando-pulando":Sprite(os.path.join('.','Personagens',self.nome,'socando-pulando.png'),(305,320),8),
                          "chutando":Sprite(os.path.join('.','Personagens',self.nome,'chutando.png'),(305,320),8),
                          "chutando-abaixado":Sprite(os.path.join('.','Personagens',self.nome,'chutando-abaixado.png'),(305,320),8),
                          "chutando-pulando":Sprite(os.path.join('.','Personagens',self.nome,'chutando-pulando.png'),(305,320),8),
                          "golpeado":Sprite(os.path.join('.','Personagens',self.nome,'golpeado.png'),(305,320),8),
                          "defesa":Sprite(os.path.join('.','Personagens',self.nome,'defesa.png'),(305,320),8),
                          "defesa-abaixado":Sprite(os.path.join('.','Personagens',self.nome,'defesa-abaixado.png'),(305,320),8),
                          "morrendo":Sprite(os.path.join('.','Personagens',self.nome,'morrendo.png'),(320,320),5),
                          "especial":Sprite(os.path.join('.','Personagens',self.nome,'especial.png'),(305,320),8),
                          "especial-abaixado":Sprite(os.path.join('.','Personagens',self.nome,'especial-abaixado.png'),(305,320),8)}

        listasomsoco = [i for i in os.listdir(os.path.join('.','Personagens',nome)) if i[:4] == 'soco' and i[-4:] == '.wav']
        self.somsoco = [pygame.mixer.Sound(os.path.join('.','Personagens',nome,i)) for i in listasomsoco]
        listasomchute = [i for i in os.listdir(os.path.join('.','Personagens',nome)) if i[:5] == 'chute' and i[-4:] == '.wav']
        self.somchute = [pygame.mixer.Sound(os.path.join('.','Personagens',nome,i)) for i in listasomchute]
        listasomapanhando = [i for i in os.listdir(os.path.join('.','Personagens',nome)) if i[:9] == 'apanhando' and i[-4:] == '.wav']
        self.somapanhando = [pygame.mixer.Sound(os.path.join('.','Personagens',nome,i)) for i in listasomapanhando]
        listasomdefesa = [i for i in os.listdir(os.path.join('.','Personagens',nome)) if i[:6] == 'defesa' and i[-4:] == '.wav']
        self.somdefesa = [pygame.mixer.Sound(os.path.join('.','Personagens',nome,i)) for i in listasomdefesa]
        listasommorrendo = [i for i in os.listdir(os.path.join('.','Personagens',nome)) if i[:8] == 'morrendo' and i[-4:] == '.wav']
        self.sommorrendo = [pygame.mixer.Sound(os.path.join('.','Personagens',nome,i)) for i in listasommorrendo]
        listasomcaindo = [i for i in os.listdir(os.path.join('.','Personagens',nome)) if i[:6] == 'caindo' and i[-4:] == '.wav']
        self.somcaindo = [pygame.mixer.Sound(os.path.join('.','Personagens',nome,i)) for i in listasomcaindo]        
        listasomespecial = [i for i in os.listdir(os.path.join('.','Personagens',nome)) if i[:8] == 'especial' and i[-4:] == '.wav']
        self.somespecial = [pygame.mixer.Sound(os.path.join('.','Personagens',nome,i)) for i in listasomespecial]  
        
        self.kcima = controles[0]
        self.kbaixo = controles[1]
        self.kesquerda = controles[2]
        self.kdireita = controles[3]
        self.ka = controles[4]
        self.kb = controles[5]
        self.kc = controles[6]
        self.hp = 150
        self.animatual = self.animacoes["parado"]
        self.caixacorpo = Rect(x,y+50,110,270)
        self.andandodireita = False
        self.andandoesquerda = False
        self.velcima = 0
        self.pulando = False
        self.abaixado = False
        self.socando = False
        self.chutando = False
        self.especial = False
        self.cooldown = 4
        self.guardabaixa = 0
        self.caixagolpe = False
        self.apanhando = False
        self.defendendo = False
        self.morto = False
        self.mortonadireita = False
        self.golpecontabilizado = False
        self.gritou = False
        self.primeiraiteracao = True

    def update(self,dtempo,eventos):
        """ Atualiza posicao, animacao, caixa de golpe e projetil do jogador """
        if self.primeiraiteracao:
            self.primeiraiteracao = False
            dtempo = 0
        if self.hp <= 0:
            self.animatual = self.animacoes["morrendo"]
            self.cooldown = 1
            if not self.gritou:
                random.choice(self.sommorrendo).play()
                self.gritou = True
                self.velcima = 1500
                
            if not self.morto:
                if self.adversario.x > self.x:
                    self.x = self.x - dtempo * 200
                    self.mortonadireita = False
                else:
                    self.x = self.x + dtempo * 200
                    self.mortonadireita = True
            
        #verifica entradas do controle
        self.input(eventos)
        #calcula movimentos do jogador
        self.movimenta(dtempo)
        #calcula colisoes de movimento, restaura ao estado anterior
        self.testacolisoes(dtempo)

        #cria caixa de golpe depedendo de como ele eh deferido e para que lado
        if (self.cooldown <= 0) and not self.golpecontabilizado:
            self.criacaixagolpe(dtempo)

        self.atualizaanimacao(dtempo)
        self.projetil.update(dtempo)

        if self.cooldown > 0: self.cooldown = self.cooldown - dtempo
        else:
            self.apanhando = False
            self.defendendo = False
        if self.guardabaixa > 0: self.guardabaixa = self.guardabaixa - dtempo

    def render(self,screen):
        """ Renderiza animacao de acordo com estado atual do jogador """
        if not self.morto:
            if self.adversario.x > self.x:
                self.animatual.render(screen,(self.x,self.y))
            else:
                self.animatual.render(screen,(self.x,self.y),(-195,0),True)
        else:
            if self.mortonadireita:
                self.animatual.render(screen,(self.x,self.y),(-195,0),True)
            else:
                self.animatual.render(screen,(self.x,self.y))

        self.projetil.render(screen)    

        #Para debug, desenha caixas de colisao, golpe e projetil
##        pygame.draw.rect(screen,(0,255,0),self.caixacorpo,1)
##        if self.caixagolpe: pygame.draw.rect(screen,(255,0,0),self.caixagolpe,1)
##        if self.projetil.caixacolisao:pygame.draw.rect(screen,(255,0,0),self.projetil.caixacolisao,1)
        

    def input(self,eventos):
        """ Trata quaisquer eventos de entradas associadas a este jogador """
        for event in eventos:
            if event.type == KEYDOWN:
                #Controles do P1
                if (event.key == self.kcima):
                    if not self.pulando and self.cooldown <= 0:
                        self.pulando = True
                        self.velcima = 2500
                elif (event.key == self.kbaixo):
                    if not self.morto: self.abaixado = True
                elif (event.key == self.kesquerda):
                    self.andandoesquerda = True
                elif (event.key == self.kdireita):
                    self.andandodireita = True
                elif (event.key == self.ka):
                    if self.cooldown <= 0:
                        self.guardabaixa = 0.4
                        if not (self.socando or self.chutando or self.especial):
                            random.choice(self.somsoco).play()
                            self.socando = True
                elif (event.key == self.kb):
                    if self.cooldown <= 0:
                        self.guardabaixa = 0.4
                        if not (self.socando or self.chutando or self.especial):
                            random.choice(self.somchute).play()
                            self.chutando = True
                elif (event.key == self.kc):
                    if (self.cooldown <= 0) and not self.projetil.caixacolisao:
                        self.guardabaixa = 0.6
                        if not (self.socando or self.chutando or self.especial ):
                            random.choice(self.somespecial).play()
                            self.especial = True
                            if (self.adversario.x > self.x):
                                self.projetil.disparar((self.x+self.caixacorpo.width,self.caixacorpo.top+10),(self.adversario.x > self.x))
                            else:
                                self.projetil.disparar((self.x-64,self.caixacorpo.top+10),(self.adversario.x > self.x))
                            
            elif event.type == KEYUP:
                #Controles do P1
                if (event.key == self.kcima):
                    pass
                elif (event.key == self.kbaixo):
                    self.abaixado = False
                elif (event.key == self.kesquerda):
                    self.andandoesquerda = False
                elif (event.key == self.kdireita):
                    self.andandodireita = False
                elif (event.key == self.ka):
                    pass
                elif (event.key == self.kb):
                    pass
                elif (event.key == self.kc):
                    pass
                
    def movimenta(self,dtempo):
        """ realiza movimentos requisitados pelos controles caso nao esteja em cooldown e calcula quedas pela gravidade """
        if self.cooldown <= 0:
            if self.andandodireita and not self.abaixado:
                self.x = self.x + dtempo * 600
                self.animatual = self.animacoes["andando"]
            elif self.andandoesquerda and not self.abaixado:
                self.x = self.x - dtempo * 600
                self.animatual = self.animacoes["andando"]
            else:
                self.animatual = self.animacoes["parado"]

            if self.pulando:
                if self.socando: self.animatual = self.animacoes["socando-pulando"]
                elif self.chutando: self.animatual = self.animacoes["chutando-pulando"]
                elif self.especial: self.animatual = self.animacoes["especial"]
                else: self.animatual = self.animacoes["pulando"]
            elif self.abaixado:
                if self.socando: self.animatual = self.animacoes["socando-abaixado"]
                elif self.chutando: self.animatual = self.animacoes["chutando-abaixado"]
                elif self.especial:
                    self.animatual = self.animacoes["especial-abaixado"]
                    self.cooldown = 0.7
                else: self.animatual = self.animacoes["abaixado"]
            elif self.socando:
                self.animatual = self.animacoes["socando"]
            elif self.chutando:
                self.animatual = self.animacoes["chutando"]
            elif self.especial:
                self.animatual = self.animacoes["especial"]
                self.cooldown = 0.7
                
        #lei da gravidade
        self.y = self.y - self.velcima * dtempo
        self.velcima = self.velcima - dtempo * 9000

    def testacolisoes(self,dtempo):
        """ executa testes de colisao e retorna o jogador a uma posicao legal caso ocorra """
        #colisao com o chao
        if self.y > self.yinicial:
            self.y = self.yinicial
            self.velcima = 0
            if self.pulando:
                self.socando = False
                self.chutando = False
                self.caixagolpe = False
                self.pulando = False
                self.golpecontabilizado = False
                self.animatual = self.animacoes["parado"]


        #atualiza caixa de corpo para colisoes
        if self.abaixado:
            self.caixacorpo.left,self.caixacorpo.top = self.x,self.y+130
            self.caixacorpo.height = 190
        else:            
            self.caixacorpo.left,self.caixacorpo.top = self.x,self.y+50
            self.caixacorpo.height = 270

        #testa colisao entre corpo dos jogadores
        if self.caixacorpo.colliderect(self.adversario.caixacorpo):
            if self.adversario.x > self.x:
                self.x = self.x - self.caixacorpo.clip(self.adversario.caixacorpo).width
            else:
                self.x = self.x + self.caixacorpo.clip(self.adversario.caixacorpo).width

        #testa colisao jogador x tela
        if self.x < 0:
            self.x = 0

        if self.x + self.caixacorpo.width > self.screenwidth:
            self.x = self.screenwidth - self.caixacorpo.width
            

        #reatualiza caixa de corpo para colisoes caso tenha sido mudada a posicao
        if self.abaixado:
            self.caixacorpo.left,self.caixacorpo.top = self.x,self.y+130
            self.caixacorpo.height = 190
        elif self.morto:
            self.caixacorpo.left,self.caixacorpo.top = self.x,self.y+240
            self.caixacorpo.height = 80 
        else:            
            self.caixacorpo.left,self.caixacorpo.top = self.x,self.y+50
            self.caixacorpo.height = 270            

    def criacaixagolpe(self,dtempo):
        """ cria uma caixa de golpe caso o jogador esteja deferindo """
        if self.socando:
            if self.adversario.x > self.x:
                if self.abaixado:
                    self.caixagolpe = Rect(self.x+self.caixacorpo.width,self.caixacorpo.top+30,100,40)
                elif self.pulando:
                    self.caixagolpe = Rect(self.x+self.caixacorpo.width,self.caixacorpo.top+30,100,100)
                else:
                    self.caixagolpe = Rect(self.x+self.caixacorpo.width,self.caixacorpo.top+30,100,40)
            else:
                if self.abaixado:
                    self.caixagolpe = Rect(self.x-100,self.caixacorpo.top+30,100,40)
                elif self.pulando:
                    self.caixagolpe = Rect(self.x-100,self.caixacorpo.top+30,100,100)
                else:
                    self.caixagolpe = Rect(self.x-100,self.caixacorpo.top+30,100,40)
        elif self.chutando:
            if self.adversario.x > self.x:
                if self.abaixado:
                    self.caixagolpe = Rect(self.x+self.caixacorpo.width,self.caixacorpo.bottom-100,130,100)
                elif self.pulando:
                    self.caixagolpe = Rect(self.x+self.caixacorpo.width,self.caixacorpo.bottom-150,70,150)
                else:
                    self.caixagolpe = Rect(self.x+self.caixacorpo.width,self.caixacorpo.bottom-150,70,150)
            else:
                if self.abaixado:
                    self.caixagolpe = Rect(self.x-130,self.caixacorpo.bottom-100,130,100)
                elif self.pulando:
                    self.caixagolpe = Rect(self.x-70,self.caixacorpo.bottom-150,70,150)
                else:
                    self.caixagolpe = Rect(self.x-70,self.caixacorpo.bottom-150,70,150)
        
    def atualizaanimacao(self,dtempo):
        """ atualiza animacao atual e testa se ja acabou para retornar ao estado anterior """
        if not self.morto and self.animatual.update(dtempo):
            if self.hp <= 0:
                self.morto = True
                self.abaixado = False
                self.animatual.frameatual = len(self.animatual.frames)-1
                random.choice(self.somcaindo).play()
            elif self.apanhando:
                self.especial = False
                self.animatual = self.animacoes["golpeado"]
            elif self.defendendo:
                if self.abaixado: self.animatual = self.animacoes["defesa-abaixado"]
                else: self.animatual = self.animacoes["defesa"]
            elif self.socando:
                if not self.pulando:
                    self.golpecontabilizado = False
                    self.socando = False
                    self.caixagolpe = False
                    if self.abaixado: self.animatual = self.animacoes["abaixado"]
                    #elif self.pulando: self.animatual = self.animacoes["pulando"]
                    else: self.animatual = self.animacoes["parado"]
                else:
                    self.animatual.frameatual = len(self.animatual.frames)-1
            elif self.chutando:
                if not self.pulando:
                    self.golpecontabilizado = False
                    self.chutando = False
                    self.caixagolpe = False
                    if self.abaixado: self.animatual = self.animacoes["abaixado"]
                    #elif self.pulando: self.animatual = self.animacoes["pulando"]
                    else: self.animatual = self.animacoes["parado"]
                else:
                    self.animatual.frameatual = len(self.animatual.frames)-1
            elif self.especial:
                self.especial = False
                self.golpecontabilizado = False
                if self.abaixado:
                    self.animatual = self.animacoes["abaixado"]
                else: self.animatual = self.animacoes["parado"]


class Projetil(object):
    """ Classe para projeteis arremessados pelos jogadores """
    def __init__(self,nome):
        """ Inicializa projetil """
        self.animacao = Sprite(nome,(400,128),8)
        self.screenwidth = pygame.display.get_surface().get_width()
        self.caixacolisao = False
        self.direita = True

    def update(self,dtempo):
        """ Atualiza posicao do projetil de acordo com velocidade """
        if self.caixacolisao:
            self.caixacolisao.left = self.caixacolisao.left + self.mult * dtempo
            if (self.caixacolisao.left >= self.screenwidth) or (self.caixacolisao.right <= 0):
                self.caixacolisao = False

        self.animacao.update(dtempo)            

    def render(self,screen):
        """ Desenha o projetil na tela """
        if self.caixacolisao:
            if self.direita:
                self.animacao.render(screen,(self.caixacolisao.left-336,self.caixacolisao.top-32),(0,0),False)
            else:
                self.animacao.render(screen,(self.caixacolisao.left,self.caixacolisao.top-32),(0,0),True)

    def disparar(self, xxx_todo_changeme1,direita):
        """ realiza o disparo de um novo projetil """
        (x,y) = xxx_todo_changeme1
        self.direita = direita
        if direita: self.mult = 500
        else: self.mult = -500
        self.caixacolisao = Rect(x,y,64,64)

    def unload(self,):
        """ decarrega elementos necessarios da classe """
        return

class Sangue(object):
    """Classe para particulas de sangue"""
    def __init__(self, xxx_todo_changeme2,limitey,direita):
        """ Inicializa particula com velocidade aleatoria """
        (x,y) = xxx_todo_changeme2
        if direita: mult = +1
        else: mult = -1

        self.limitey = limitey   
        self.velx = random.randint(40,800)*mult
        self.vely = random.randint(40,1000)
        self.x = x
        self.y = y
        self.tempo = 0
        self.cor = random.randint(150,255)

    def update(self,dtempo):
        """ Atualiza posicao da particula pela velocidade """
        self.y = self.y - self.vely * dtempo
        if self.y > self.limitey:
            self.y = self.limitey
            self.velx = 10
        
        self.x = self.x + self.velx * dtempo
        #lei da gravidade
        self.vely = self.vely - dtempo * 4000

        self.tempo = self.tempo + dtempo

    def render(self,screen):
        """ Desenha a particula na tela como um pequeno circulo """
        pygame.draw.circle(screen,(self.cor,0,0),(int(self.x),int(self.y)),2)

    def unload(self,):
        """ decarrega elementos necessarios da classe """
        pass


class Barra(object):
    """Classe para barras de contagem de hp"""
    def __init__(self, xxx_todo_changeme3,width,height,jogador,invertida = False):
        """ Inicializa barra de contagem """
        (x,y) = xxx_todo_changeme3
        self.nome = jogador.nome
        self.font = pygame.font.Font(os.path.join('.','Imagens',"fonte.ttf"),int(0.04*pygame.display.get_surface().get_height()))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jogador = jogador
        self.unidade = (float(width) / jogador.hp)
        if invertida:
            self.inversor = -1
            self.retanguloverde = Rect(x+width,y,self.unidade*jogador.hp*self.inversor,height)
            self.retangulovermelho = Rect(x+width,y,self.unidade*jogador.hp*self.inversor,height)
        else:
            self.inversor = 1
            self.retanguloverde = Rect(x,y,self.unidade*jogador.hp,height)
            self.retangulovermelho = Rect(x,y,self.unidade*jogador.hp,height)
        self.tensao = 3
        self.corverde = 255
        self.inccorverde = -self.tensao
        self.corvermelho = 255
        self.inccorvermelho = -10
        self.tamanhovermelho = float(width*self.inversor)

    def update(self,dtempo):
        """ Atualiza tamanho da barra """
        self.retanguloverde.width = self.unidade*self.jogador.hp*self.inversor
        if (self.retangulovermelho.width*self.inversor) > (self.retanguloverde.width*self.inversor):
            self.tamanhovermelho = self.tamanhovermelho - (dtempo*((self.tamanhovermelho - self.retanguloverde.width)/self.width)*200)
            self.retangulovermelho.width = int(self.tamanhovermelho)

        self.corverde = self.corverde + self.inccorverde
        self.corvermelho = self.corvermelho + self.inccorvermelho

        #varia a velocidade com que pisca a barra de acordo com seu tamanho       
        if self.corverde <= 150: self.inccorverde = self.tensao
        if self.corvermelho <= 170: self.inccorvermelho = 10

        if self.corverde >= 255:
            self.corverde = 255
            self.inccorverde = -self.tensao
        if self.corvermelho >= 255:
            self.corvermelho = 255
            self.inccorvermelho = -3

        if (self.retanguloverde.width*self.inversor) <= (self.width/2):
            self.tensao = int(60 - ((self.retanguloverde.width*self.inversor)/(self.width/2.)) * 50.)

        
    def render(self,screen):
        """ Desenha a barra de hp e a barra vermelha auxiliar no fundo """
        if not self.jogador.hp <= 0:
            pygame.draw.rect(screen,(self.corvermelho,0,0),self.retangulovermelho)
            pygame.draw.rect(screen,(0,self.corverde,0),self.retanguloverde)
        screen.blit(self.font.render(self.nome, True, (self.corvermelho,0,0)),(self.x,self.y - 30))            

    def unload(self,):
        """ decarrega elementos necessarios da classe """
        return


class Vitoria(object):
    """Classe para frase de vitoria e retrato do jogador """
    def __init__(self, nome, player):
        """ Inicializa personagem vitorioso """
        self.tela = pygame.display.get_surface()
        self.area = self.tela.get_rect()
        self.width = self.tela.get_width()
        self.height = self.tela.get_height()
        #Carrega personagem vitorioso e sua frase
        self.foto = Sprite(os.path.join('.','Personagens', nome, "vs.png"),(0,0),False,(self.width*0.5,self.height*0.598333333))
        frases = []
        with open(os.path.join('.', 'Personagens', nome, "frases.txt")) as arqfrases:
            frases = arqfrases.readlines()
        if sys.platform[:-2] == "win":
            self.frase = "  "+random.choice(frases)[:-1]+"  "
        else:
            self.frase = "  "+random.choice(frases)[:-2]+"  "
        self.player = player
        self.y = (self.height * 0.41)
        #Player 1 vai da esquerda para a direita
        if self.player == 1:
            self.x = -self.width*0.5
            self.velx = 1000.
        #Player 2 vai da direita para a esquerda
        else:
            self.x = self.width
            self.velx = -1000.
        self.movimentar = False
        self.timer = 1.
        self.retornando = False
        self.font = pygame.font.Font(os.path.join('.','Imagens',"fonte.ttf"), int(0.036*self.height))

    def update(self,dtempo):
        """ Movimenta o retrato e a frase em direcoes contrarias e aceleradas """
        if self.movimentar:
            self.x = self.x + (self.velx * dtempo)
            #Player 1 vai da esquerda para a direita
            if self.player == 1:
                if self.velx >= 1 and not self.retornando:
                    self.velx = self.velx - dtempo*1000
                else:
                    self.velx = self.velx + dtempo*1000
                    if not self.retornando:
                        self.x = 0.1545 * self.width
                        self.retornando = True
                        self.timer = 3
                        self.movimentar = False
            #Player 2 vai da direita para a esquerda
            else:
                if self.velx <= -1 and not self.retornando:
                    self.velx = self.velx + dtempo*1000
                else:
                    self.velx = self.velx - dtempo*1000
                    if not self.retornando:
                        self.x = 0.34575 * self.width
                        self.retornando = True
                        self.timer = 3
                        self.movimentar = False
        if self.timer <= 0: self.movimentar = True
        else: self.timer = self.timer - dtempo
        
    def render(self,screen):
        """ Desenha o retrato do jogador vitorioso e sua frase """
        if (self.x <= screen.get_width()) and (self.x >= (-self.width*0.5)):
            self.foto.render(screen, (self.x,self.y), (0,0), (self.player == 2))
            if self.player == 1:
                screen.blit(self.font.render(self.frase, True, (200,0,0),(0,0,0)),(self.width*0.5 - self.x*2.5,self.y+((self.height*0.598333333)/1.5)))
            else:
                screen.blit(self.font.render(self.frase, True, (200,0,0),(0,0,0)),(self.width - self.x*2.5,self.y+((self.height*0.598333333)/1.5)))

    def unload(self,):
        """ Descarrega elementos da frase de vitoria """
        return

class Chuvadebits(object):
    """ Classe que gera chuva de bits """
    def __init__(self, quantidade):
        """ Inicializa os bits no topo da tela """
        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height()
        
        self.retangulos = [Rect( (203/800.)*self.width , (159/600.)*self.height , (21/800.)*self.width, (69/600.)*self.height),# Barra lateral do F
                           Rect( (203/800.)*self.width , (159/600.)*self.height , (52/800.)*self.width, (16/600.)*self.height),# Barra superior do F
                           Rect( (203/800.)*self.width , (186/600.)*self.height , (48/800.)*self.width, (12/600.)*self.height),# Barra do meio do F
                           Rect( (268/800.)*self.width , (159/600.)*self.height , (21/800.)*self.width, (69/600.)*self.height),# I
                           Rect( (302/800.)*self.width , (159/600.)*self.height , (20/800.)*self.width, (69/600.)*self.height),# Barra lateral do G
                           Rect( (302/800.)*self.width , (159/600.)*self.height , (66/800.)*self.width, (20/600.)*self.height),# Barra superior do G
                           Rect( (302/800.)*self.width , (216/600.)*self.height , (66/800.)*self.width, (12/600.)*self.height),# Barra inferior do G
                           Rect( (352/800.)*self.width , (189/600.)*self.height , (20/800.)*self.width, (40/600.)*self.height),# Barra direita do G
                           Rect( (332/800.)*self.width , (188/600.)*self.height , (33/800.)*self.width, (16/600.)*self.height),# Barra do meio do G
                           Rect( (384/800.)*self.width , (159/600.)*self.height , (21/800.)*self.width, (69/600.)*self.height),# Barra esquerda do H
                           Rect( (430/800.)*self.width , (159/600.)*self.height , (21/800.)*self.width, (69/600.)*self.height),# Barra direita do H
                           Rect( (385/800.)*self.width , (183/600.)*self.height , (64/800.)*self.width, (16/600.)*self.height),# Barra do meio do H
                           Rect( (459/800.)*self.width , (159/600.)*self.height , (64/800.)*self.width, (16/600.)*self.height),# Barra de cima do T
                           Rect( (482/800.)*self.width , (159/600.)*self.height , (20/800.)*self.width, (70/600.)*self.height),# Barra do meio do T
                           Rect( (564/800.)*self.width , (159/600.)*self.height , (22/800.)*self.width, (40/600.)*self.height),# Barra da !
                           Rect( (564/800.)*self.width , (211/600.)*self.height , (22/800.)*self.width, (16/600.)*self.height)] # Ponto da !
        self.bits = []
        self.letras = []
        self.font = pygame.font.Font(os.path.join('.','Imagens',"fonte.ttf"), int(0.034*self.height))
        self.primeiraiteracao = True
        self.tempo = 0
        self.tocoufight = False
        self.corverde = 255
        self.inccorverde = -5
        for i in range(quantidade):
            self.bits.append({'x':random.randint(-5,self.width),'y':random.randint(-1000,-500),'vel':(random.randint(2200,3500)/100.),
                              'velx':random.randint(-3500,3500)/100.,
                              'vely':random.randint(-3500,1500)/100.,
                              'num':random.choice(['0','1']),'parado':0})

    def update(self,dtempo):
        """ Atualiza posicao dos bits """
        #ignoramos o primeiro dtempo pois ele eh acrescido do tempo de load
        if self.primeiraiteracao:
            self.primeiraiteracao = False
            dtempo = 0
        self.tempo = self.tempo + dtempo
        for i in self.bits:
            if not i['parado']:
                i['y'] = i['y'] + (i['vel'] * dtempo * 20)
                for n in self.retangulos:
                    if n.collidepoint(i['x'],i['y']):
                        i['parado'] = random.randint(0,3)
        self.bits = [i for i in self.bits if i['y'] <= self.height]
        if self.tempo >= 4:
            if not self.tocoufight:
                self.tocoufight = True
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.Sound(os.path.join('.','Sons',"fight.wav")).play()
                pygame.mixer.Sound(os.path.join('.','Sons',"estourofight.wav")).play()
                
            for i in self.bits:
                if i['parado']:
                    i['x'] = i['x'] + (i['velx'] * dtempo * 20)
                    i['y'] = i['y'] + (i['vely'] * dtempo * 20)
                    i['vely'] = i['vely'] + (dtempo * 50)
        if self.tempo >=6:
            self.bits = []

        self.corverde = self.corverde + self.inccorverde
        if (self.corverde >= 255):
            self.corverde = 255
            self.inccorverde = self.inccorverde * (-1)
        elif (self.corverde <=200):
            self.inccorverde = self.inccorverde * (-1)
        
    def render(self,screen):
        """ Desenha os bits na tela """
        for i in self.bits:
            screen.blit(self.font.render(i['num'], True, (0,self.corverde,0)),(i['x'],i['y']))
        #for i in self.retangulos:
        #    pygame.draw.rect(screen,(255,0,0),i,1)
                    

    def unload(self,):
        """ Descarrega chuva de bits """
        return

