from matplotlib import pyplot as plt
import min_bbox
import numpy as np


cores = [[0, 191, 255], [124, 252, 0], [210, 105, 30], [255, 0, 0], [0, 100, 0], [70, 130, 180], [102, 205, 170], [210, 105, 30], [238, 130, 238], [255, 160, 122]]


# Se for amarelo trasforma em vermelho e verifica o vizinho, se o viziho não for amarelo, nem vermelho, então é uma borda
def verifica_vizinhos(imagem, linha, coluna, lista, lista_borda):
    imagem[linha][coluna] = [255, 0, 0]
    lista.append((linha, coluna))  # Todos os pontos da ilha
    for i in range(linha - 1, linha + 2):
        for j in range(coluna - 1, coluna + 2):
            if i >= 0 and i <= len(imagem) - 1 and j >= 0 and j <= len(imagem[0]) - 1:  # Verifica se o ponto está dentro da matriz
                if imagem[i][j][0] == 36 and imagem[i][j][1] == 231 and imagem[i][j][2] == 253:  # Amarelo
                    verifica_vizinhos(imagem, i, j, lista, lista_borda)
                elif imagem[i][j][0] != 255 and imagem[i][j][1] != 0 and imagem[i][j][2] != 0 and (linha == i or coluna == j):
                    lista_borda.append((linha, coluna))


def coloca_paineis(imagem, tamanho_painel, retangulo, borda_rotacionada, cor):
    espacamento_horizontal = 1.5*tamanho_painel[0]
    espacamento_vertical = 1.1*tamanho_painel[1]

    eixos = min_bbox.rotaciona_contorno([[1, 0], [0, 1]], -retangulo.angulo)
    eixos = [np.array(e) for e in eixos]

    ponto_inicial = np.array(borda_rotacionada[0])
    limite_horizontal = espacamento_horizontal
    limite_vertical = 0
    num_paineis = 0
    while True:
        if verifica_painel(imagem, tamanho_painel, ponto_inicial, eixos[0], eixos[1], cor):
            desenha_painel(tamanho_painel, ponto_inicial, eixos[0], eixos[1])
            num_paineis += 1
        limite_vertical += espacamento_vertical
        if limite_vertical + tamanho_painel[1] > retangulo.lados[1]:
            ponto_inicial = np.array(borda_rotacionada[0]) + limite_horizontal*eixos[0]
            if limite_horizontal > retangulo.lados[0]:
                break
            if verifica_painel(imagem, tamanho_painel, ponto_inicial, eixos[0], eixos[1], cor):
                desenha_painel(tamanho_painel, ponto_inicial, eixos[0], eixos[1])
                num_paineis += 1
            limite_horizontal += espacamento_horizontal
            limite_vertical = espacamento_vertical
        ponto_inicial = ponto_inicial+(espacamento_vertical)*(eixos[1])
    return num_paineis


def segmenta_imagem(imagem):
    n = 0
    for i in range(len(imagem)):
        for j in range(len(imagem[0])):
            lista = []
            borda = []
            if imagem[i][j][0] == 36 and imagem[i][j][1] == 231 and imagem[i][j][2] == 253:  # Amarelo
                verifica_vizinhos(imagem, i, j, lista, borda)
                if len(lista) < 300:  # Retirar ilhas pequenas
                    continue
                for k in range(len(lista)):
                    linha = lista[k][0]
                    coluna = lista[k][1]
                    imagem[linha][coluna] = cores[n]

                yield borda, cores[n]

                n += 1
                if n >= len(cores):
                    n = 0


def num_paineis(imagem, tam_painel):
    total_paineis = 0

    for borda, cor in segmenta_imagem(imagem):
        caixa = min_bbox.Retangulo(float("inf"))
        extremos_rotacionados = min_bbox.acha_min_bbox(borda, caixa)
        total_paineis += coloca_paineis(imagem, tam_painel, caixa, extremos_rotacionados, cor)

    return total_paineis


def ponto_valido(imagem, x, y, cor):
    i = int(x)
    j = int(y)
    if i < 0 or j < 0 or i >= len(imagem) or j >= len(imagem):
        return False
    return imagem[i][j][0] == cor[0] and imagem[i][j][1] == cor[1] and imagem[i][j][2] == cor[2]


def verifica_painel(imagem, tam_painel_pixel, ponto_inicial, eixo_0, eixo_1, cor):
    for k in range(5):
        p = ponto_inicial + k*(tam_painel_pixel[1]/4)*eixo_1
        for _ in range(6):
            if not ponto_valido(imagem, p[0], p[1], cor):
                return False
            p += (tam_painel_pixel[0]/2)*eixo_0
    return True


def desenha_painel(tam_painel_pixel, ponto_inicial, eixo_1, eixo_2):
    p0 = ponto_inicial
    p1 = eixo_1*tam_painel_pixel[0] + p0
    p2 = eixo_2*tam_painel_pixel[1] + p0
    p3 = p1 + p2 - p0
    plt.plot([p0[1], p1[1]], [p0[0], p1[0]], 'g')
    plt.plot([p1[1], p3[1]], [p1[0], p3[0]], 'g')
    plt.plot([p3[1], p2[1]], [p3[0], p2[0]], 'g')
    plt.plot([p2[1], p0[1]], [p2[0], p0[0]], 'g')
