import folium
import contornos
import paineis

# HOSPITAL DAS CLINICAS DA UNICAMP DE CAMPINAS
# LATITUDE = -22.8269585
# LONGITUDE = -47.064116

# HOSPITAL MUNICIPAL JOSANIAS CASTANHA BRAGA
# LATITUDE = -23.8232741
# LONGITUDE = -46.7263557

# HOSPITAL ESTADUAL DE SUMARÉ
# LATITUDE = -22.816655
# LONGITUDE = -47.2416309

# HOSPITAL MUNICIPAL CARMEN PRUDENTE OU Hospital Municipal Cidade Tiradentes
# LATITUDE = -23.5971845
# LONGITUDE = -46.4036324

# HOSPITAL ESTADUAL DE VILA ALPINA ORG SOCIAL SECONCI SAO PAULO
# LATITUDE = -23.5929081
# LONGITUDE = -46.5607168

# HOSPITAL ESTADUAL AMERICO BRASILIENSE
LATITUDE = -21.7410705
LONGITUDE = -48.1220018

# HOSPITAL UNIVERSITARIO DA USP SAO PAULO
# LATITUDE = -23.5649363
# LONGITUDE = -46.7405751

# HOSP MUN TIDE SETUBAL
# LATITUDE = -23.4971439
# LONGITUDE = -46.4399994

EFICIENCIA = 0.211  # sem unidade
IRRADIACAO = 1904.1  # unidade: kWh/m²
LARGURA = 2.256  # unidade: m
ALTURA = 1.133  # unidade: m
AREA_MOD = LARGURA*ALTURA


def calcula_energia_produzida(area_mod, num_mod, inc_radiacao, efic_mod):
    energ_prod_por_mod = area_mod*inc_radiacao*efic_mod  # unidade: kWh/ano
    energ_total_prod = (energ_prod_por_mod/12)*num_mod*0.8  # unidade: kWh/mes
    return energ_total_prod


mapa = folium.Map([LATITUDE, LONGITUDE], zoom_start=19, max_zoom=20)

estilo = {'fillColor': '#FF0000', 'color': '#FF0000'}

propriedade = contornos.obtem_contorno_propriedade(LATITUDE, LONGITUDE)
predios = contornos.obtem_contornos_telhados(LATITUDE, LONGITUDE)

if propriedade is not None:
    folium.GeoJson(propriedade).add_to(mapa)

quant_paineis = 0

for i, pol in enumerate(predios):
    folium.GeoJson(predios[i], style_function=lambda x: estilo).add_to(mapa)
    quant_paineis += paineis.coloca_paineis((LARGURA, ALTURA), pol, mapa)

if not predios and propriedade is not None:
    quant_paineis = paineis.coloca_paineis((LARGURA, ALTURA), propriedade, mapa)

energia = calcula_energia_produzida(AREA_MOD, quant_paineis, IRRADIACAO, EFICIENCIA)
print(f"Energia produzida por mês: {energia} kWh/mes")
print("Quantidade de paineis:", quant_paineis)

mapa.show_in_browser()
