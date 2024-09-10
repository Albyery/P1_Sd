import pygame

class Movimentar:
    def __init__(self, tamanho_tela, tamanho_jogador, tamanho_bola):
        self.tamanho_tela = tamanho_tela
        self.tamanho_jogador = tamanho_jogador
        self.tamanho_bola = tamanho_bola

    def movimentar_jogadores(self, jogador, jogador2):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and jogador.x + self.tamanho_jogador < self.tamanho_tela[0]:
            jogador.x += 5
        if keys[pygame.K_LEFT] and jogador.x > 0:
            jogador.x -= 5
        if keys[pygame.K_d] and jogador2.x + self.tamanho_jogador < self.tamanho_tela[0]:
            jogador2.x += 5
        if keys[pygame.K_a] and jogador2.x > 0:
            jogador2.x -= 5

    @staticmethod
    def movimentar_bola(bola, movimento_bola):
        bola.x += movimento_bola[0]
        bola.y += movimento_bola[1]
        return bola
