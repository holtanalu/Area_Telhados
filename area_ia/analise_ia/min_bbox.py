import numpy as np
from matplotlib import pyplot as plt


class Retangulo:
    def __init__(self, area):
        self.extremos = []
        self.angulo = 0
        self.area = area
        self.lados = []


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


def acha_min_bbox(borda, retangulo):
    for k in range(90):
        borda_rotacionada = rotaciona_contorno(borda, (np.pi * float(k))/180)
        b_box = encontra_b_box(borda_rotacionada)
        area = (b_box[2] - b_box[0])*(b_box[3] - b_box[1])
        if area < retangulo.area:
            retangulo.area = area
            retangulo.extremos = [(b_box[0], b_box[1]), (b_box[0], b_box[3]), (b_box[2], b_box[3]), (b_box[2], b_box[1])]
            retangulo.angulo = (np.pi * float(k))/180
            retangulo.lados = [(b_box[2] - b_box[0]), (b_box[3] - b_box[1])]
    extremos_rotacionados = rotaciona_contorno(retangulo.extremos, -retangulo.angulo)

    # Desenha a retangulo
    plt.plot([extremos_rotacionados[0][1], extremos_rotacionados[1][1]], [extremos_rotacionados[0][0], extremos_rotacionados[1][0]], 'w')
    plt.plot([extremos_rotacionados[1][1], extremos_rotacionados[2][1]], [extremos_rotacionados[1][0], extremos_rotacionados[2][0]], 'w')
    plt.plot([extremos_rotacionados[2][1], extremos_rotacionados[3][1]], [extremos_rotacionados[2][0], extremos_rotacionados[3][0]], 'w')
    plt.plot([extremos_rotacionados[3][1], extremos_rotacionados[0][1]], [extremos_rotacionados[3][0], extremos_rotacionados[0][0]], 'w')

    return extremos_rotacionados
