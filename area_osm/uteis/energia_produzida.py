def energia_produzida(area_mod, inc_radiacao, efic_mod, area_telhado):
    num_mod = int(area_telhado/area_mod)
    print(num_mod)
    energ_prod_por_mod = area_mod*inc_radiacao*efic_mod
    energ_total_prod = (energ_prod_por_mod/12)*num_mod*0.8

    return energ_total_prod


Am = 2.56
n = 0.211
Is = 1904.1

# Cálculo da energia total produzida por módulo - IA
energia_IA = energia_produzida(Am, Is, n, 7547.232)

# Cálculo da energia total produzida por módulo - Área do poligono
energia_area_estimada = energia_produzida(Am, Is, n, 7909)

# area util 3157.6

# Cálculo da energia total produzida por módulo - usina
energia_usina = energia_produzida(Am, Is, n, 26542.9)

print("energia estimada com a área da IA: ", energia_IA)
print("energia estimada com a área do poligono: ", energia_area_estimada)
print("energia estimada com a usina: ", energia_usina)
