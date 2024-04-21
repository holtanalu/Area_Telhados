import paineis
import pandas as pd
import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt


LARGURA = 2.56  # unidade: m
ALTURA = 1.33  # unidade: m


def metros_para_pixels(valor_metros, lat_cen, zoom):
    circ_terra = 40075000
    metros_por_pixel = (np.cos(np.pi*lat_cen/180)*circ_terra)/(np.power(2, 8 + zoom))
    return valor_metros/metros_por_pixel


def calcula_energia_produzida(area_mod, num_mod, inc_radiacao=1904.1, efic_mod=0.211):
    energ_prod_por_mod = area_mod*inc_radiacao*efic_mod  # unidade: kWh/ano
    energ_total_prod = (energ_prod_por_mod/12)*num_mod*0.8  # unidade: kWh/mes
    return energ_total_prod


def main():
    sys.setrecursionlimit(100000)
    resultados = open('resultados.csv', 'w')
    resultados.write("hospital,energia")
    tabela = pd.read_csv("latitudes.csv")
    for lat, hosp in zip(tabela['lat'], tabela["hosp"]):
        print(f"\rColocando paineis no hospital {hosp}", end="")
        imagem = cv2.imread(f'../res/res/hosp{hosp}.png')
        alt_pixel = metros_para_pixels(ALTURA, lat, 18)
        lar_pixel = metros_para_pixels(LARGURA, lat, 18)
        tam_painel = np.array([alt_pixel, lar_pixel])
        total_paineis = paineis.num_paineis(imagem, tam_painel)
        energia = calcula_energia_produzida(ALTURA*LARGURA, total_paineis)
        resultados.write(f'{hosp},{energia}\n')
        # plt.imshow(imagem)
        # plt.savefig(f"../paineis/hospital{hosp}.pdf")
        # plt.show()
        plt.close()
    print()


if __name__ == "__main__":
    main()
