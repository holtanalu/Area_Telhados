from matplotlib import pyplot as plt
import numpy as np
import cv2
import sys

cores = [[0, 191, 255], [124, 252, 0], [210, 105, 30], [255, 0, 0], [0, 100, 0], \
         [70, 130, 180], [102, 205, 170], [210, 105, 30], [238, 130, 238], [255, 160, 122]]


def verifica_vizinhos(imagem, linha, coluna, lista, lista_borda):
    imagem[linha][coluna] = [255, 0, 0]
    lista.append((linha, coluna))
    for i in range(linha - 1, linha + 2):
        for j in range(coluna - 1, coluna + 2):
            if i >= 0 and i <= len(imagem) - 1 and j >= 0 and j <= len(imagem[0]) - 1:  # Verifica se o ponto está dentro da matriz
                if imagem[i][j][0] == 36 and imagem[i][j][1] == 231 and imagem[i][j][2] == 253:
                    verifica_vizinhos(imagem, i, j, lista, lista_borda)
                elif imagem[i][j][0] != 255 and imagem[i][j][1] != 0 and imagem[i][j][2] != 0 and (linha == i or coluna == j):
                    lista_borda.append((linha, coluna))


def encontra_b_box(lista_borda):
    min_i = 500
    max_i = 0
    min_j = 500
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


def rotaciona_contorno(lista_borda, angulo):
    lista_rotacionada = []
    for i in range(len(lista_borda)):
        lista_rotacionada.append((
            lista_borda[i][0]*np.cos(angulo) + lista_borda[i][1]*np.sin(angulo),
            -lista_borda[i][0]*np.sin(angulo) + lista_borda[i][1]*np.cos(angulo)
            ))
    return lista_rotacionada


def segmentacao(imagem):
    n = 0
    for i in range(len(imagem)):
        for j in range(len(imagem[0])):
            lista = []
            borda = []
            if imagem[i][j][0] == 36 and imagem[i][j][1] == 231 and imagem[i][j][2] == 253:
                verifica_vizinhos(imagem, i, j, lista, borda)
                if len(lista) < 300:
                    continue
                for k in range(len(lista)):
                    linha = lista[k][0]
                    coluna = lista[k][1]
                    imagem[linha][coluna] = cores[n]
                n += 1
                if n >= len(cores):
                    n = 0
                borda_rotacionada = rotaciona_contorno(borda, np.pi/6)
                b_box = encontra_b_box(borda_rotacionada)
                pontos_extremos = [(b_box[0], b_box[1]), (b_box[0], b_box[3]), (b_box[2], b_box[3]), (b_box[2], b_box[1])]
                extremos_rotacionados = rotaciona_contorno(pontos_extremos, -np.pi/6)

                plt.plot([extremos_rotacionados[0][1], extremos_rotacionados[1][1]], [extremos_rotacionados[0][0], extremos_rotacionados[1][0]], 'w')
                plt.plot([extremos_rotacionados[1][1], extremos_rotacionados[2][1]], [extremos_rotacionados[1][0], extremos_rotacionados[2][0]], 'w')
                plt.plot([extremos_rotacionados[2][1], extremos_rotacionados[3][1]], [extremos_rotacionados[2][0], extremos_rotacionados[3][0]], 'w')
                plt.plot([extremos_rotacionados[3][1], extremos_rotacionados[0][1]], [extremos_rotacionados[3][0], extremos_rotacionados[0][0]], 'w')


def main():
    sys.setrecursionlimit(100000)
    imagem = cv2.imread('teste_rel_ia.png')
    # print(imagem[150][150])
    segmentacao(imagem)
    plt.imshow(imagem)
    plt.show()

    # roxo [84  1 68]
    # amarelo [ 36 231 253]


if __name__ == "__main__":
    main()
