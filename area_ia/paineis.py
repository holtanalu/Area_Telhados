from matplotlib import pyplot as plt
import cv2
import sys

cores = [[0, 191, 255], [124, 252, 0], [210, 105, 30], [255, 0, 0], [0, 100, 0], [70, 130, 180], [102, 205, 170], [210, 105, 30], [238, 130, 238], [255, 160, 122]]


def verifica_vizinhos(imagem, linha, coluna, n):
    imagem[linha][coluna] = n
    for i in range(linha - 1, linha + 2):
        for j in range(coluna - 1, coluna + 2):
            if i >= 0 and i <= len(imagem) - 1 and j >= 0 and j <= len(imagem[0]) - 1 and imagem[i][j][0] == 36 and imagem[i][j][1] == 231 and imagem[i][j][2] == 253:
                verifica_vizinhos(imagem, i, j, n)


def segmentacao(imagem):
    n = cores[0]
    k = 0
    for i in range(len(imagem)):
        for j in range(len(imagem[0])):
            if imagem[i][j][0] == 36 and imagem[i][j][1] == 231 and imagem[i][j][2] == 253:
                verifica_vizinhos(imagem, i, j, n)
                k += 1
                if k >= len(cores):
                    k = 0
                n = cores[k]


# def print_imagem(imagem):
#     for i in range(len(imagem)):
#         print(imagem[i])


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
