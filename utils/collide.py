from config import movimento_bola  # ou variaveis import movimento_bola


class Collide:
    def __init__(self, som_colisao, som_pontuacao):
        self.som_colisao = som_colisao
        self.som_pontuacao = som_pontuacao

    def verificar_colisao_bordas(self, bola, movimento_bola, tamanho_tela, tamanho_bola):
        # Inverte a direção da bola se ela tocar nas bordas da tela
        if bola.x <= 0 or bola.x + tamanho_bola >= tamanho_tela[0]:
            movimento_bola[0] = -movimento_bola[0]  # Colisão nas laterais
            self.som_colisao.play()
        if bola.y <= 0 or bola.y + tamanho_bola >= tamanho_tela[1]:
            movimento_bola[1] = -movimento_bola[1]  # Colisão nas bordas superior e inferior
            self.som_colisao.play()

        return movimento_bola

    @staticmethod
    def verificar_colisao_jogadores(bola, jogador, jogador2, movimento_bola):
        ultimo_rebatedor = None
        # Colisão com o jogador 1
        if bola.colliderect(jogador):
            movimento_bola[1] = -movimento_bola[1]  # Inverte a direção vertical da bola
            ultimo_rebatedor = 'jogador1'

        # Colisão com o jogador 2
        elif bola.colliderect(jogador2):
            movimento_bola[1] = -movimento_bola[1]  # Inverte a direção vertical da bola
            ultimo_rebatedor = 'jogador2'

        # Verifica se os jogadores estão ocupando o mesmo espaço e ajusta suas posições
        if jogador.colliderect(jogador2):
            if jogador.x > jogador2.x:
                jogador.x += 5  # Move o jogador 1 para a direita
            else:
                jogador2.x += 5  # Move o jogador 2 para a direita

        return ultimo_rebatedor

    def verificar_colisao_blocos(self, bola, blocos, ultimo_rebatedor, pontuacao_jogador1, pontuacao_jogador2):
        colisao = False
        for bloco in blocos[:]:
            if bola.colliderect(bloco):
                blocos.remove(bloco)
                movimento_bola[1] = -movimento_bola[1]
                self.som_pontuacao.play()
                colisao = True
                if ultimo_rebatedor == 'jogador1':
                    pontuacao_jogador1 += 1
                elif ultimo_rebatedor == 'jogador2':
                    pontuacao_jogador2 += 1
                # Inverte a direção da bola na colisão com o bloco
                return True, pontuacao_jogador1, pontuacao_jogador2

        return False, pontuacao_jogador1, pontuacao_jogador2
