import folium
import contornos
import paineis


LATITUDE = -22.816655
LONGITUDE = -47.2416309
EFICIENCIA = 0.211  # sem unidade
IRRADIACAO = 1904.1  # unidade: kWh/m²
LARGURA = 2.256  # unidade: m
ALTURA = 1.133  # unidade: m
AREA_MOD = LARGURA*ALTURA


def calcula_energia_produzida(area_mod, num_mod, inc_radiacao, efic_mod):
    energ_prod_por_mod = area_mod*inc_radiacao*efic_mod  # unidade: kWh/ano
    energ_total_prod = (energ_prod_por_mod/12)*num_mod*0.8  # unidade: kWh/mes
    return energ_total_prod


mapa = folium.Map([LATITUDE, LONGITUDE], zoom_start=19, max_zoom=30, tiles='CartoDb dark_matter')

estilo = {'fillColor': '#FF0000', 'color': '#FF0000'}

propriedade = contornos.obtem_contorno_propriedade(LATITUDE, LONGITUDE)
predios = contornos.obtem_contornos_telhados(LATITUDE, LONGITUDE)

folium.GeoJson(propriedade).add_to(mapa)

quant_paineis = 0

for i, pol in enumerate(predios):
    folium.GeoJson(predios[i], style_function=lambda x: estilo).add_to(mapa)
    quant_paineis += paineis.coloca_paineis((LARGURA, ALTURA), pol, mapa)

if not predios:
    quant_paineis = paineis.coloca_paineis((LARGURA, ALTURA), propriedade, mapa)

energia = calcula_energia_produzida(AREA_MOD, quant_paineis, IRRADIACAO, EFICIENCIA)
print(energia)
print(quant_paineis)

mapa.show_in_browser()
