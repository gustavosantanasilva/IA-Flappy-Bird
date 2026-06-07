# Importando Bibliotecas Necesarias

import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800


# Imagens do jogo

IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('Game/imgs' , 'pipe.png')))

IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('Game/imgs' , 'base.png')))

IMG_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('Game/imgs' , 'bg.png')))

IMGS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('Game/imgs' , 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('Game/imgs' , 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('Game/imgs' , 'bird3.png')))
]

# Fontes do jogo
pygame.font.init()
FONT_PONTO = pygame.font.SysFont('arial',50)


# Objetos 

class Passaro:
    IMGS = IMGS_PASSARO

    #Animaçãoes da rotação
    ROTACAO_MAX = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    #atributos passaro
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_img = 0
        self.imagem = self.IMGS[0]


    def pular(self):
        self.velocidade = 10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #calcular deslocamento

        

        pos_centro_img = self.imagem.get_rect(topleft=(self.x, self.y)).center
        self.tempo += 1
        

    def desenhar(self, tela):
        # 1. Pega a posição atual do mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Faz com que o pássaro siga a posição do mouse (centralizado no cursor)
        self.x = mouse_x
        self.y = mouse_y

        # 2. Definir imagem do passaro (Animação)
        self.contagem_img += 1

        if self.contagem_img < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_img < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_img < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_img < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_img < self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_img = 0

        # 3. Lógica para não bater asa se estiver caindo (Opcional)
        # Se você tiver uma variável de ângulo ou velocidade vertical (self.velocidade),
        # pode forçar self.imagem = self.IMGS[1] aqui caso esteja caindo muito rápido.

        # 4. Criar o retângulo alinhado com o mouse e desenhar
        # Usamos o 'center' para que o meio do pássaro fique exatamente na ponta do mouse
        retangulo = self.imagem.get_rect(center=(self.x, self.y))
        
        # Desenha a imagem na tela usando a posição do retângulo corrigida
        tela.blit(self.imagem, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)



class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posicao_topo = 0
        self.posicao_base = 0
        self.cano_topo = pygame.transform.flip(IMG_CANO, False, True)
        self.cano_base =  IMG_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.posicao_topo = self.altura - self.cano_topo.get_height()
        self.posicao_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x  -= self.VELOCIDADE
    
    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.posicao_topo))
        tela.blit(self.cano_base, (self.x, self.posicao_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.posicao_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.posicao_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if topo_ponto or base_ponto:
            return True
        else:
            return False
        
    
class Chao:
    VELOCIDADE = 5
    LARGURA =  IMG_CHAO.get_width()
    IMAGEM = IMG_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):

        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x2 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

    
def desenhar_tela(tela, passaros, canos, chao,  pontos):
    pygame.mouse.set_visible(False)
    tela.blit(IMG_FUNDO, (0,0))
    for passaro in passaros:
        passaro.desenhar(tela)
    
    for cano in canos:
        cano.desenhar(tela)

    texto = FONT_PONTO.render(f"Pontuação : {pontos}", 1,(255, 255, 255))
    tela.blit(texto,  (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela1 = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    tela = tela1
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)


        # Interação com o usuario / controles

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        
        #Mover os objetos e o cenario

        for passaro in passaros:
            passaro.mover()

        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i,passaro in  enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            
            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)

        
        if adicionar_cano:
            pontos+=1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)

        
        for  i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)


        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()