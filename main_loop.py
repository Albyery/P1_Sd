import pygame

# Inicializa o Pygame
pygame.init()

# Inicializa o mixer de som
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
qtde_total_blocos = qtde_linhas_blocos * qtde_blocos_linha

# Pontuações dos jogadores
pontuacao_jogador1 = 0
pontuacao_jogador2 = 0


def criar_blocos(qtd_blocos_linha, qtd_linhas_blocos):
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / qtd_blocos_linha - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10
    brick = []
    for j in range(qtd_linhas_blocos):
        for i in range(qtd_blocos_linha):
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco,
                                altura_bloco)
            brick.append(bloco)
    return brick


cores = {
    'azul': (0, 0, 255),
    'branco': (255, 255, 255),
    'preto': (0, 0, 0),
    'verde': (0, 255, 0),
    'vermelho': (255, 0, 0)
}

movimento_bola = [3, -3]
ultimo_rebatedor = None


def desenhar_inicio_jogo():
    tela.fill(cores["preto"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.rect(tela, cores['vermelho'], jogador2)
    pygame.draw.rect(tela, cores["branco"], bola)


def desenhar_blocos(blocks):
    for bloco in blocks:
        pygame.draw.rect(tela, cores["verde"], bloco)


def movimentar_jogadores():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and jogador.x + tamanho_jogador < tamanho_tela[0]:
        jogador.x += 5
        if jogador.colliderect(jogador2):
            jogador.x -= 5
    if keys[pygame.K_LEFT] and jogador.x > 0:
        jogador.x -= 5
        if jogador.colliderect(jogador2):
            jogador.x += 5
    if keys[pygame.K_d] and jogador2.x + tamanho_jogador < tamanho_tela[0]:
        jogador2.x += 5
        if jogador2.colliderect(jogador):
            jogador2.x -= 5
    if keys[pygame.K_a] and jogador2.x > 0:
        jogador2.x -= 5
        if jogador2.colliderect(jogador):
            jogador2.x += 5


som_colisao = pygame.mixer.Sound('Music/collide_block.mp3')
som_pontuacao = pygame.mixer.Sound('Music/collide_score.mp3')
som_vencedor = pygame.mixer.Sound('Music/winning.mp3')


def movimentar_bola(ball):
    global ultimo_rebatedor, pontuacao_jogador1, pontuacao_jogador2
    movimento = movimento_bola
    ball.x += movimento[0]
    ball.y += movimento[1]

    if ball.x <= 0 or ball.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = -movimento[0]
        som_colisao.play()
    if ball.y <= 0 or ball.y + tamanho_bola >= tamanho_tela[1]:
        movimento[1] = -movimento[1]
        som_colisao.play()
    if ball.colliderect(jogador):
        movimento[1] = -movimento[1]
        som_colisao.play()
        ultimo_rebatedor = 'jogador1'
    elif ball.colliderect(jogador2):
        movimento[1] = -movimento[1]
        som_colisao.play()
        ultimo_rebatedor = 'jogador2'

    for bloco in blocos[:]:
        if ball.colliderect(bloco):
            blocos.remove(bloco)
            som_pontuacao.play()
            movimento[1] = -movimento[1]
            if ultimo_rebatedor == 'jogador1':
                pontuacao_jogador1 += 1
            elif ultimo_rebatedor == 'jogador2':
                pontuacao_jogador2 += 1

    return movimento


def atualizar_pontuacao():
    fonte = pygame.font.Font(None, 30)
    texto_jogador1 = fonte.render(f'Jogador 1: {pontuacao_jogador1}', 1, cores['azul'])
    texto_jogador2 = fonte.render(f'Jogador 2: {pontuacao_jogador2}', 1, cores['vermelho'])
    tela.blit(texto_jogador1, (0, 660))
    tela.blit(texto_jogador2, (560, 660))

    return True if len(blocos) == 0 else False


blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)


def desenhar_tela_final():
    tela.fill(cores["preto"])
    fonte = pygame.font.Font(None, 50)
    som_vencedor.play()
    if pontuacao_jogador1 > pontuacao_jogador2:
        mensagem_vencedor = fonte.render("Jogador 1 Venceu!", 1, cores['azul'])
    elif pontuacao_jogador2 > pontuacao_jogador1:
        mensagem_vencedor = fonte.render("Jogador 2 Venceu!", 1, cores['vermelho'])
    else:
        mensagem_vencedor = fonte.render("Empate!", 1, cores['branco'])
    tela.blit(mensagem_vencedor, (220, 330))

    # Desenhar o botão de reiniciar
    fonte_botao = pygame.font.Font(None, 36)
    botao_reiniciar = pygame.Rect(270, 400, 150, 50)
    pygame.draw.rect(tela, cores['branco'], botao_reiniciar)
    texto_reiniciar = fonte_botao.render("Reiniciar", 1, cores['preto'])
    tela.blit(texto_reiniciar, (295, 410))
    pygame.display.flip()

    return botao_reiniciar


# Função principal
def main_loop():
    fim_jogo = False

    # Carrega a música e sons
    pygame.mixer.music.load("Music/main_theme.mp3")  # Certifique-se de que o caminho está correto
    pygame.mixer.music.play(-1)  # Toca a música em loop

    while not fim_jogo:
        desenhar_inicio_jogo()
        desenhar_blocos(blocos)

        fim_jogo = atualizar_pontuacao()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

        movimentar_jogadores()
        movimentar_bola(bola)

        pygame.time.wait(10)
        pygame.display.flip()

    # Para a música ao finalizar o jogo
    pygame.mixer.music.stop()

    # Tela final
    botao_reiniciar = desenhar_tela_final()

    esperando_reiniciar = True
    while esperando_reiniciar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_reiniciar.collidepoint(evento.pos):
                    # Reiniciar o jogo
                    reiniciar_jogo()
                    return


def reiniciar_jogo():
    global bola, jogador, jogador2, pontuacao_jogador1, pontuacao_jogador2, blocos
    bola = pygame.Rect(345, 345, tamanho_bola, tamanho_bola)
    jogador = pygame.Rect(0, 550, tamanho_jogador, 15)
    jogador2 = pygame.Rect(610, 550, tamanho_jogador, 15)
    pontuacao_jogador1 = 0
    pontuacao_jogador2 = 0
    blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)
    main_loop()


# Inicia o jogo
main_loop()

# Finaliza o Pygame
pygame.quit()
