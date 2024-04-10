from matplotlib import pyplot as plt
import numpy as np
import math
import cv2
import sys

LARGURA = 2.56  # unidade: m
ALTURA = 1.33  # unidade: m

cores = [[0, 191, 255], [124, 252, 0], [210, 105, 30], [255, 0, 0], [0, 100, 0], \
         [70, 130, 180], [102, 205, 170], [210, 105, 30], [238, 130, 238], [255, 160, 122]]


class Retangulo:
    def __init__(self, area):
        self.extremos = []
        self.angulo = 0
        self.area = area
        self.lados = []


def metros_para_pixels(valor_metros, lat_cen, zoom):
    circ_terra = 40075000
    metros_por_pixel = (np.cos(np.pi*lat_cen/180)*circ_terra)/(np.power(2, 8 + zoom))
    print(metros_por_pixel*250)
    return valor_metros/metros_por_pixel


def magnitude(vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))


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


def encontra_b_box(lista_borda):
    min_i = 1e8
    max_i = 0
    min_j = 1e8
    max_j = 0
    for k in range(len(lista_borda)):
        linha = lista_borda[k][0]
        coluna = lista_borda[k][1]
        if linha < min_i:
            min_i = linha
        if linha > max_i:
            max_i = linha
        if coluna < min_j:
            min_j = coluna
        if coluna > max_j:
            max_j = coluna
    return [min_i, min_j, max_i, max_j]


# Transformação linear para rotacionar os pontos
def rotaciona_contorno(lista_borda, angulo):
    lista_rotacionada = []
    for i in range(len(lista_borda)):
        lista_rotacionada.append((
            lista_borda[i][0]*np.cos(angulo) + lista_borda[i][1]*np.sin(angulo),
            -lista_borda[i][0]*np.sin(angulo) + lista_borda[i][1]*np.cos(angulo)
            ))
    return lista_rotacionada


# Função para segmentar a imagem em ilhas
def segmentacao(imagem):
    n = 0
    alt_pixel = metros_para_pixels(ALTURA, -22.328863, 19)
    lar_pixel = metros_para_pixels(LARGURA, -22.328863, 19)

    tam_painel = np.array([alt_pixel, lar_pixel])

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
                n += 1
                if n >= len(cores):
                    n = 0

                # Achar minima B_box
                caixa = Retangulo(float("inf"))
                for k in range(90):
                    borda_rotacionada = rotaciona_contorno(borda, (np.pi * float(k))/180)
                    b_box = encontra_b_box(borda_rotacionada)
                    area = (b_box[2] - b_box[0])*(b_box[3] - b_box[1])
                    if area < caixa.area:
                        caixa.area = area
                        caixa.extremos = [(b_box[0], b_box[1]), (b_box[0], b_box[3]), (b_box[2], b_box[3]), (b_box[2], b_box[1])]
                        caixa.angulo = (np.pi * float(k))/180
                        caixa.lados = [(b_box[2] - b_box[0]), (b_box[3] - b_box[1])]
                extremos_rotacionados = rotaciona_contorno(caixa.extremos, -caixa.angulo)

                # Desenha a caixa
                plt.plot([extremos_rotacionados[0][1], extremos_rotacionados[1][1]], [extremos_rotacionados[0][0], extremos_rotacionados[1][0]], 'w')
                plt.plot([extremos_rotacionados[1][1], extremos_rotacionados[2][1]], [extremos_rotacionados[1][0], extremos_rotacionados[2][0]], 'w')
                plt.plot([extremos_rotacionados[2][1], extremos_rotacionados[3][1]], [extremos_rotacionados[2][0], extremos_rotacionados[3][0]], 'w')
                plt.plot([extremos_rotacionados[3][1], extremos_rotacionados[0][1]], [extremos_rotacionados[3][0], extremos_rotacionados[0][0]], 'w')
       
                espacamento_horizontal = 1.5*tam_painel[0]
                espacamento_vertical = 1.1*tam_painel[1]

                eixos = rotaciona_contorno([[1, 0], [0, 1]], -caixa.angulo)
                eixos = [np.array(e) for e in eixos]
                print(tam_painel)
                ponto_inicial = np.array(extremos_rotacionados[0])
                limite_horizontal = espacamento_horizontal
                limite_vertical = 0
                num_paineis = 0
                while True:
                    if verifica_painel(imagem, tam_painel, ponto_inicial, eixos[0], eixos[1]):
                        desenha_painel(tam_painel, ponto_inicial, eixos[0], eixos[1])
                        num_paineis += 1
                    limite_vertical += espacamento_vertical
                    if limite_vertical + tam_painel[1] > caixa.lados[1]:
                        ponto_inicial = np.array(extremos_rotacionados[0]) + limite_horizontal*eixos[0]
                        if limite_horizontal > caixa.lados[0]:
                            break
                        if verifica_painel(imagem, tam_painel, ponto_inicial, eixos[0], eixos[1]):
                            desenha_painel(tam_painel, ponto_inicial, eixos[0], eixos[1])
                            num_paineis += 1
                        limite_horizontal += espacamento_horizontal
                        limite_vertical = espacamento_vertical
                    ponto_inicial = ponto_inicial+(espacamento_vertical)*(eixos[1])
                print(f"Foram colocados {num_paineis} paineis")


def ponto_invalido(imagem, x, y):
    i = int(x)
    j = int(y)
    return imagem[i][j][0] == 84 and imagem[i][j][1] == 1 and imagem[i][j][2] == 68 


def verifica_painel(imagem, tam_painel_pixel, ponto_inicial, eixo_0, eixo_1):
    for k in range(5):
        p = ponto_inicial + k*(tam_painel_pixel[1]/4)*eixo_1
        for _ in range(4):
            if ponto_invalido(imagem, p[0], p[1]):
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


def main():
    sys.setrecursionlimit(100000)
    imagem = cv2.imread('teste_rel_ia.png')
    segmentacao(imagem)
    plt.imshow(imagem)
    plt.show()

    # roxo [84  1 68]
    # amarelo [ 36 231 253]


if __name__ == "__main__":
    main()
