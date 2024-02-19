# Python program to find convex hull of a set of points. Refer
# https://www.geeksforgeeks.org/orientation-3-ordered-points/
# for explanation of orientation()
# This code is contributed by
# Akarsh Somani, IIIT Kalyani

# classe de ponto com x, y como ponto


def indice_esquerda(points):

    # Encontrando o ponto mais à esquerda

    minn = 0
    for i in range(1, len(points)):
        if points[i][0] < points[minn][0]:
            minn = i
        elif points[i][0] == points[minn][0]:
            if points[i][1] > points[minn][1]:
                minn = i
    return minn


def orientation(p, q, r):

    # Para encontrar a orientação do trio ordenado (p, q, r).
    #  A função retorna os seguintes valores
    #  0 -> p, q e r são colineares
    #  1 --> Sentido horário
    #  2 --> Sentido anti-horário

    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def convexHull(points, n):

    # Deve haver pelo menos 3 pontos
    if n < 3:
        return

    # Encontre o ponto mais à esquerda
    p_inicial = indice_esquerda(points)

    hull = []

    # Comece do ponto mais à esquerda, continue movendo no sentido anti-horário
    # até chegar ao ponto inicial novamente. Este loop executa O(h)
    # vezes onde h é o número de pontos no resultado ou saída.

    p = p_inicial
    q = 0

    while True:

        # Add current point to result
        hull.append(p)

        # Procure um ponto 'q' tal que a orientação(p, q,
        # x) seja anti-horário para todos os pontos 'x'. A ideia
        # é manter o controle do último visitado que esta mais no sentido anti-horário
        # Se algum ponto 'i' for mais anti-horário que q, então atualize q.

        q = (p + 1) % n

        for i in range(n):

            # Se eu estiver mais no sentido anti-horário
            # que o q atual, então atualize q
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        # Agora q é o mais anti-horário em relação a p
        # Defina p como q para a próxima iteração, de modo que q seja adicionado a
        # resultado 'hull'

        p = q

        # Enquanto não chegamos ao primeiro ponto
        if p == p_inicial:
            break

    # Imprimir resultado
    pol_convexo = []
    for each in hull:
        pol_convexo.append((points[each][1], points[each][0]))
        # print(points[each][0], points[each][1])

    return pol_convexo
