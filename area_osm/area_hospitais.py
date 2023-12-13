import pandas as pd
import osmnx as ox
import folium

from shapely.geometry import Point
from area import area
from geopy import Nominatim


def num_para_string_com_virgula(num):
    if num is not None:
        return str(num).replace(".", ",")


def cria_dicionario(poligono):
    x, y = poligono.exterior.coords.xy
    lista_poligono = []

    for i, j in zip(x, y):
        lista_poligono.append((i, j))

    dicionario = {'type': 'Polygon', 'coordinates': [lista_poligono]}
    return dicionario


def contorno_propriedade(lat, lon):
    tags = {'amenity': True, "addr:street": True}
    coordenadas = [lat, lon]

    predios = ox.geometries_from_point(coordenadas, tags, dist=300)
    predios = predios[predios.geom_type == 'Polygon'][:2000]

    for pol in predios['geometry']:
        if pol.contains(Point(lon, lat)):
            return pol


def obtem_area_propriedade(lat, lon, mapa):
    tags = {'amenity': True}
    coordenadas = [lat, lon]

    predios = ox.geometries_from_point(coordenadas, tags, dist=300)
    predios = predios[predios.geom_type == 'Polygon'][:2000]

    for i, pol in enumerate(predios['geometry']):
        if pol.contains(Point(lon, lat)):
            folium.GeoJson(predios[i:i+1]).add_to(mapa)
            return area(cria_dicionario(pol))


def obtem_area_telhado(lat, lon, mapa):
    tags = {'building': True}
    coordenadas = [lat, lon]
    area_total = 0

    estilo = {'fillColor': '#FF0000', 'color': '#FF0000'}

    predios = ox.geometries_from_point(coordenadas, tags, dist=300)
    predios = predios[predios.geom_type == 'Polygon'][:2000]
    propriedade = contorno_propriedade(lat, lon)

    for i, pol in enumerate(predios['geometry']):
        if propriedade is not None and propriedade.contains(pol):
            if mapa:
                folium.GeoJson(predios[i:i+1], style_function=lambda x: estilo).add_to(mapa)
            area_total += area(cria_dicionario(pol))
        elif pol.contains(Point(lon, lat)):
            if mapa:
                folium.GeoJson(predios[i:i+1], style_function=lambda x: estilo).add_to(mapa)
            return area(cria_dicionario(pol))

    if area_total != 0:
        return area_total


def cria_tabela_areas(tabela):
    tabela_completa = open('tabelas/tabela_revisada.txt', 'w')
    mapa = folium.Map([-22.041695112321737, -48.59185325493342], zoom_start=8, tiles='CartoDb dark_matter')

    hospitais = pd.read_csv(tabela)
    tabela_completa.write('NOME;LATITUDE;LONGITUDE;CIDADE;AREA PROPRIEDADE;\
                            AREA TELHADO;LINKS OSM;LINKS MAPS\n')

    for linha in range(len(hospitais)):
        nome_hospital = hospitais['NOME'].iloc[linha]

        lat = hospitais['LATITUDE'].iloc[linha]
        lon = hospitais['LONGITUDE'].iloc[linha]

        lugar = Nominatim(user_agent="myGeocoder").reverse(f"{lat}, {lon}")
        endereco = lugar.raw['address']

        lat_virgula = num_para_string_com_virgula(lat)
        lon_virgula = num_para_string_com_virgula(lon)

        cidade = 'não encontrada'
        if 'city' in endereco.keys():
            cidade = endereco["city"]
        elif 'town' in endereco.keys():
            cidade = endereco["town"]

        area_propriedade = num_para_string_com_virgula(obtem_area_propriedade(lat, lon, mapa))
        area_telhado = num_para_string_com_virgula(obtem_area_telhado(lat, lon, mapa))
        links_osm = f"https://www.openstreetmap.org/#map=19/{lat}/{lon}"
        links_maps = f"https://www.google.com.br/maps/@{lat},{lon},18z"

        if area_propriedade is None and area_telhado is None:
            folium.CircleMarker(location=(lat, lon), radius=3, color='green').add_to(mapa)

        tabela_completa.write(f'{nome_hospital};{lat_virgula};{lon_virgula};{cidade};\
                              {area_propriedade};{area_telhado};{links_osm};{links_maps}\n')

        print(linha)

    mapa.show_in_browser()
    mapa.save("hospitais_contorno.html")
    tabela_completa.close()


cria_tabela_areas('tabelas/tabela_completa.csv')
