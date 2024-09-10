import pygame
from utils.desenha_objetos import DesenharObjetos
from utils.movimentar import Movimentar
from utils.collide import Collide
from utils.config import movimento_bola  # ou variaveis import movimento_bola

# Inicializações
pygame.init()
pygame.mixer.init()

tamanho_tela = (690, 690)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Brick Breaker")

tamanho_bola = 10
bola = pygame.Rect(345, 345, tamanho_bola, tamanho_bola)

tamanho_jogador = 80
jogador = pygame.Rect(0, 550, tamanho_jogador, 15)
jogador2 = pygame.Rect(610, 550, tamanho_jogador, 15)

qtde_blocos_linha = 8
qtde_linhas_blocos = 5
cores = {
    'azul': (0, 0, 255),
    'branco': (255, 255, 255),
    'preto': (0, 0, 0),
    'verde': (0, 255, 0),
    'vermelho': (255, 0, 0)
}

# Sons
som_colisao = pygame.mixer.Sound('Music/collide_block.mp3')
som_pontuacao = pygame.mixer.Sound('Music/collide_score.mp3')
som_vencedor = pygame.mixer.Sound('Music/winning.mp3')

# Classes
desenha_objetos = DesenharObjetos(tela, cores)
movimentar = Movimentar(tamanho_tela, tamanho_jogador, tamanho_bola)
collide = Collide(som_colisao, som_pontuacao)

movimentar_bola = movimento_bola
pontuacao_jogador1 = 0
pontuacao_jogador2 = 0
ultimo_rebatedor = None


def criar_blocos():
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / qtde_blocos_linha - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10
    blocos = []
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas,
                                largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos


blocos = criar_blocos()


def main_loop():
    fim_jogo = False
    pygame.mixer.music.load("Music/main_theme.mp3")
    pygame.mixer.music.play(-1)

    global bola, movimentar_bola, pontuacao_jogador1, pontuacao_jogador2, ultimo_rebatedor, blocos

    while not fim_jogo:
        desenha_objetos.desenhar_inicio_jogo(jogador, jogador2, bola)
        desenha_objetos.desenhar_blocos(blocos)
        desenha_objetos.desenhar_pontuacao(pontuacao_jogador1, pontuacao_jogador2)

        movimentar_bola = collide.verificar_colisao_bordas(bola, movimentar_bola, tamanho_tela, tamanho_bola)
        ultimo_rebatedor = collide.verificar_colisao_jogadores(bola, jogador, jogador2, movimento_bola)
        colisao, pontuacao_jogador1, pontuacao_jogador2 = collide.verificar_colisao_blocos(bola, blocos,
                                                                                           ultimo_rebatedor,
                                                                                           pontuacao_jogador1,
                                                                                           pontuacao_jogador2)

        if len(blocos) == 0:
            fim_jogo = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        movimentar.movimentar_jogadores(jogador, jogador2)
        bola = movimentar.movimentar_bola(bola, movimento_bola)

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.mixer.music.stop()
    botao_reiniciar = desenha_objetos.desenhar_tela_final(pontuacao_jogador1, pontuacao_jogador2, som_vencedor)

    esperando_reiniciar = True
    while esperando_reiniciar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_reiniciar.collidepoint(evento.pos):
                    reiniciar_jogo()
                    return


def reiniciar_jogo():
    global bola, jogador, jogador2, pontuacao_jogador1, pontuacao_jogador2, blocos, movimento_bola
    bola = pygame.Rect(345, 345, tamanho_bola, tamanho_bola)
    jogador = pygame.Rect(0, 550, tamanho_jogador, 15)
    jogador2 = pygame.Rect(610, 550, tamanho_jogador, 15)
    pontuacao_jogador1 = 0
    pontuacao_jogador2 = 0
    blocos = criar_blocos()
    movimento_bola = [3, -3]
    main_loop()


# Inicia o jogo
main_loop()

# Finaliza o Pygame
pygame.quit()
