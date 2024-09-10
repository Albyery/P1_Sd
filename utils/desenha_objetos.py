import pygame

class DesenharObjetos:
    def __init__(self, tela, cores):
        self.tela = tela
        self.cores = cores

    def desenhar_inicio_jogo(self, jogador1, jogador2, bola):
        # Preenche o fundo da tela
        self.tela.fill(self.cores['preto'])
        # Desenha os jogadores e a bola
        pygame.draw.rect(self.tela, self.cores['azul'], jogador1)
        pygame.draw.rect(self.tela, self.cores['vermelho'], jogador2)
        pygame.draw.rect(self.tela, self.cores['branco'], bola)

    def desenhar_blocos(self, blocos):
        # Desenha os blocos
        for bloco in blocos:
            pygame.draw.rect(self.tela, self.cores['verde'], bloco)

    def desenhar_pontuacao(self, pontuacao_jogador1, pontuacao_jogador2):
        # Atualiza e desenha a pontuação dos jogadores na tela
        fonte = pygame.font.Font(None, 30)
        texto_jogador1 = fonte.render(f'Jogador 1: {pontuacao_jogador1}', True, self.cores['azul'])
        texto_jogador2 = fonte.render(f'Jogador 2: {pontuacao_jogador2}', True, self.cores['vermelho'])
        self.tela.blit(texto_jogador1, (10, 660))
        self.tela.blit(texto_jogador2, (500, 660))

    def desenhar_tela_final(self, pontuacao_jogador1, pontuacao_jogador2, som_vencedor):
        # Preenche a tela de preto
        self.tela.fill(self.cores["preto"])
        fonte = pygame.font.Font(None, 50)

        # Toca o som de vitória
        som_vencedor.play()

        # Verifica quem venceu
        if pontuacao_jogador1 > pontuacao_jogador2:
            mensagem_vencedor = fonte.render("Jogador 1 Venceu!", True, self.cores['azul'])
        elif pontuacao_jogador2 > pontuacao_jogador1:
            mensagem_vencedor = fonte.render("Jogador 2 Venceu!", True, self.cores['vermelho'])
        else:
            mensagem_vencedor = fonte.render("Empate!", True, self.cores['branco'])

        # Desenha a mensagem de vencedor
        self.tela.blit(mensagem_vencedor, (220, 330))

        # Desenha o botão de reiniciar
        fonte_botao = pygame.font.Font(None, 36)
        botao_reiniciar = pygame.Rect(270, 400, 150, 50)
        pygame.draw.rect(self.tela, self.cores['branco'], botao_reiniciar)
        texto_reiniciar = fonte_botao.render("Reiniciar", True, self.cores['preto'])
        self.tela.blit(texto_reiniciar, (295, 410))
        pygame.display.flip()

        return botao_reiniciar
