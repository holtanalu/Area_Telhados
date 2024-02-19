import numpy as np


class Retangulo:
    def __init__(self, area):
        self.extremos = []
        self.eixos = []
        self.area = area
        self.origem = 0


def normaliza_vec(vetor):
    return vetor / np.linalg.norm(vetor)


def produto_interno(vetor1, vetor2):
    return np.dot(vetor1, vetor2, out=None)


def cria_vetor(vetor1, vetor2):
    x = vetor1[0] - vetor2[0]
    y = vetor1[1] - vetor2[1]
    return np.array([x, y])


def minima_bbox(poligono_convexo):
    retangulo = Retangulo(1e8)
    n = len(poligono_convexo)
    for i in range(n):
        # Criando novo sistema de coordenadas
        origem = poligono_convexo[i]
        eixo_u = cria_vetor(poligono_convexo[(i+1) % n], origem)
        eixo_u = normaliza_vec(eixo_u)
        eixo_v = np.array([eixo_u[1], -eixo_u[0]])

        # Setando extremos
        min_u = 0
        max_u = 0
        max_v = 0  # min_v é garantido ser 0

        # Criando a caixa no novo sistema de coordenadas
        for j in range(n):
            vetor = cria_vetor(poligono_convexo[j], origem)
            dot = produto_interno(eixo_u, vetor)
            if dot < min_u:
                min_u = dot
            elif dot > max_u:
                max_u = dot
            dot = produto_interno(eixo_v, vetor)
            if dot > max_v:
                max_v = dot

        # Verificando menor área
        area = (max_u - min_u)*max_v
        if area < retangulo.area:
            retangulo.area = area
            # Localizando extremos
            ext_1 = (eixo_u*min_u) + origem
            ext_2 = (eixo_u*max_u) + origem
            ext_3 = (eixo_u*min_u) + (eixo_v*max_v) + origem
            ext_4 = (eixo_u*max_u) + (eixo_v*max_v) + origem
            retangulo.extremos = [ext_1, ext_2, ext_4, ext_3]
            retangulo.eixos = [eixo_u, eixo_v]
            retangulo.origem = origem
    return retangulo
