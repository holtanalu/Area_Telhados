import fecho_convexo as fc
import min_bbox
import folium
import numpy as np
from shapely.geometry import Point


def desenha_pol(mapa, pontos, cor):
    folium.Polygon(pontos, color=cor).add_to(mapa)


def encontra_retangulo(ponto, largura, altura, eixo_u, eixo_v):
    p1 = ponto + metros_para_lat_lon(largura*eixo_u, ponto[0])
    p2 = ponto + metros_para_lat_lon(altura*eixo_v, ponto[0]) + metros_para_lat_lon(largura*eixo_u, ponto[0])
    p3 = ponto + metros_para_lat_lon(altura*eixo_v, ponto[0])
    extremos = [ponto, p1, p2, p3]
    return extremos


def metros_para_lat_lon(vetor, reference_lat):
    # Raio médio da Terra em metros
    raio_terra = 6378137.0

    # Conversão de metros para graus de coordenadas
    delta_lat = (vetor[0] / raio_terra) * (180 / np.pi)
    delta_lon = (vetor[1] / raio_terra) * (180 / np.pi) / np.cos(reference_lat * np.pi/180)

    return np.array([delta_lat, delta_lon])


def lat_lon_para_metros(coord1, coord2):
    raio_terra = 6378137.0

    dlat = ((coord2[0] * np.pi) / 180) - ((coord1[0] * np.pi) / 180)
    dlon = ((coord2[1] * np.pi) / 180) - ((coord1[1] * np.pi) / 180)

    a = (np.sin(dlat/2) ** 2) + ((((coord1[1] * np.pi) / 180) ** 2) * (np.sin(dlon/2) ** 2))
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return raio_terra*c


def verifica_contem_poligono(pontos, poligono):
    for i in range(len(pontos)):
        if poligono.contains(Point(pontos[i][1], pontos[i][0])):
            continue
        else:
            return False
    return True


def coloca_paineis(dimensoes, poligono, mapa):
    lon, lat = poligono.exterior.coords.xy
    pontos = list(zip(lon, lat))
    poligono_convexo = fc.convexHull(pontos, len(pontos))
    desenha_pol(mapa, poligono_convexo, "yellow")

    retangulo = min_bbox.minima_bbox(poligono_convexo)
    print(retangulo.extremos)
    desenha_pol(mapa, retangulo.extremos, "green")

    ponto_inicial = retangulo.extremos[0]
    primeiro_ponto = ponto_inicial

    num_linhas = int(lat_lon_para_metros(ponto_inicial, retangulo.extremos[3])/3)
    num_colunas = int(lat_lon_para_metros(ponto_inicial, retangulo.extremos[1])/dimensoes[0]) - 1
    num_paineis = 0

    for i in range(num_colunas):
        for j in range(num_linhas):
            if j % 2 == 0:
                cor = "red"
            else:
                cor = "green"
            extremos = encontra_retangulo(ponto_inicial, dimensoes[0], dimensoes[1], retangulo.eixos[0], retangulo.eixos[1])
            if verifica_contem_poligono(extremos, poligono):
                desenha_pol(mapa, extremos, cor)
                num_paineis += 1
            ponto_inicial = ponto_inicial + metros_para_lat_lon(3*retangulo.eixos[1], ponto_inicial[0])
        ponto_inicial = primeiro_ponto + metros_para_lat_lon(1.2*dimensoes[0]*retangulo.eixos[0], primeiro_ponto[0])
        primeiro_ponto = ponto_inicial

    return num_paineis
