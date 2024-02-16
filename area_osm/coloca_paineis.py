import fecho_convexo as fc
import min_bbox
import folium
import numpy as np


def desenha_pol(mapa, pontos, cor):
    folium.Polygon(pontos, color=cor).add_to(mapa)


def desenha_retangulo(mapa, ponto, largura, altura, eixo_u, eixo_v):
    p1 = ponto + meters_to_lat_lon(largura*eixo_u, ponto[0])
    p2 = ponto + meters_to_lat_lon(altura*eixo_v, ponto[0]) + meters_to_lat_lon(largura*eixo_u, ponto[0])
    p3 = ponto + meters_to_lat_lon(altura*eixo_v, ponto[0])
    extremos = [ponto, p1, p2, p3]
    desenha_pol(mapa, extremos, "red")


def meters_to_lat_lon(vetor, reference_lat):
    # Raio médio da Terra em metros
    earth_radius = 6378137.0

    # Conversão de metros para graus de coordenadas
    delta_lat = (vetor[0] / earth_radius) * (180 / np.pi)
    delta_lon = (vetor[1] / earth_radius) * (180 / np.pi) / np.cos(reference_lat * np.pi/180)

    return np.array([delta_lat, delta_lon])


mapa = folium.Map([-22.816655, -47.2416309], zoom_start=20, tiles='CartoDb dark_matter')
poligono = fc.obtem_contorno_propriedade(-22.816655, -47.2416309)
folium.GeoJson(poligono).add_to(mapa)

lon, lat = poligono.exterior.coords.xy
pontos = list(zip(lon, lat))
poligono_convexo = fc.convexHull(pontos, len(pontos))
desenha_pol(mapa, poligono_convexo, "yellow")

retangulo = min_bbox.minima_bbox(poligono_convexo)
print("oi")
print(retangulo.extremos)
desenha_pol(mapa, retangulo.extremos, "green")

desenha_retangulo(mapa, retangulo.extremos[0], 100, 60, retangulo.eixos[0], retangulo.eixos[1])

mapa.show_in_browser()
