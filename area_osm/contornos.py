import osmnx as ox
from shapely.geometry import Point


def obtem_contorno_propriedade(lat, lon):
    tags = {'amenity': True, "addr:street": True}
    coordenadas = [lat, lon]

    predios = ox.geometries_from_point(coordenadas, tags, dist=300)
    predios = predios[predios.geom_type == 'Polygon'][:2000]

    for pol in predios['geometry']:
        if pol.contains(Point(lon, lat)):
            return pol


def obtem_contornos_telhados(lat, lon):
    tags = {'building': True}
    coordenadas = [lat, lon]

    predios = ox.geometries_from_point(coordenadas, tags, dist=300)
    predios = predios[predios.geom_type == 'Polygon'][:2000]
    propriedade = obtem_contorno_propriedade(lat, lon)

    lista_telhados = []

    for pol in predios['geometry']:
        if propriedade is not None and propriedade.contains(pol):
            lista_telhados.append(pol)
        elif pol.contains(Point(lon, lat)):
            lista_telhados.append(pol)

    return lista_telhados
