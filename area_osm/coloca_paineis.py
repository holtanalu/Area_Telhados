import fecho_convexo as fc
import min_bbox
import folium


def desenha_pol(mapa, pontos, cor):
    folium.Polygon(pontos, color=cor).add_to(mapa)


def desenha_retangulo(mapa, ponto, largura, altura, eixo_u, eixo_v):
    p1 = ponto + altura*eixo_u
    p2 = ponto + (largura*eixo_v) + (altura*eixo_u)
    p3 = ponto + largura*eixo_v
    extremos = [ponto, p1, p2, p3]
    desenha_pol(mapa, extremos, "red")


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

desenha_retangulo(mapa, retangulo.extremos[0], 0.0005, 0.0003, retangulo.eixos[0], retangulo.eixos[1])

mapa.show_in_browser()
