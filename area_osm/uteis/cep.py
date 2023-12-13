from geopy.geocoders import Nominatim
import pandas as pd


def buscar_cep(tabela):
    hospitais = pd.read_csv(tabela)

    for linha in range(len(hospitais)):

        lat = hospitais['LATITUDE'].iloc[linha]
        lon = hospitais['LONGITUDE'].iloc[linha]

        geolocator = Nominatim(user_agent="teset")
        location = geolocator.reverse(f'{lat},{lon}')
        full_address = str(location.address)
        print(full_address)
        print("\n")
        # endereco = full_address.split()
        # cep = endereco[-2].replace(",", " ")
        # print(cep)
        # cep = [ad for ad in full_address.split() if ad.find('-') != -1][0]
        # print("cep =", cep)


buscar_cep('../tabelas/teste.text')
