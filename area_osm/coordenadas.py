import pandas as pd

from geopy.geocoders import GoogleV3
from chave_api_geocoding import API_KEY


def coordenadas_hospitais(tabela, chave):
    hospitais = pd.read_csv(tabela)

    for linha in range(len(hospitais)):
        nome_hospital = hospitais['nome_estabelecimento_saude'].iloc[linha]

        geo_localizador = GoogleV3(api_key=chave)
        local = geo_localizador.geocode(nome_hospital, timeout=100)

        if local:
            lat = local.latitude
            lon = local.longitude
            print(nome_hospital, lat, lon)


chave = API_KEY
coordenadas_hospitais('tabelas/hospitais_publicos.csv', chave)
