import turtle


def get_mouse_click_coor(x, y):
    print(x, y)
    tartaruga.setpos(x, y)
    pontos.append((x, y))
    tartaruga.pendown()


def space():
    tartaruga.pensize(0)
    tartaruga.speed(10)
    tartaruga.shape('blank')
    tartaruga.penup()
    tartaruga.setpos(-largura/2, -altura/2)
    tartaruga.pendown()
    tartaruga.fillcolor("black")
    tartaruga.begin_fill()
    tartaruga.setpos(-largura/2, altura/2)
    tartaruga.setpos(largura/2, altura/2)
    tartaruga.setpos(largura/2, -altura/2)
    tartaruga.setpos(-largura/2, -altura/2)
    tartaruga.end_fill()
    tartaruga.penup()

    for i in range(len(poligonos)):
        tartaruga.begin_fill()
        if cor[i] == 1:
            tartaruga.fillcolor("white")
        else:
            tartaruga.fillcolor("black")
        for j in range(len(poligonos[i])):
            tartaruga.setpos(poligonos[i][j][0], poligonos[i][j][1])
            tartaruga.pendown()
        tartaruga.setpos(poligonos[i][0][0], poligonos[i][0][1])
        tartaruga.end_fill()
        tartaruga.penup()

    tartaruga.screen.getcanvas().postscript(file="duck.eps")


def branco():
    tartaruga.setpos(pontos[0][0], pontos[0][1])
    tartaruga.penup()
    poligonos.append(pontos.copy())
    cor.append(1)
    pontos.clear()


def preto():
    tartaruga.setpos(pontos[0][0], pontos[0][1])
    tartaruga.penup()
    poligonos.append(pontos.copy())
    cor.append(0)
    pontos.clear()


pontos = []
poligonos = []
cor = []

largura, altura = 857, 724
screen = turtle.Screen()
screen.setup(largura, altura)

tartaruga = turtle.Turtle()
tartaruga.shape("turtle")

tartaruga.penup()
tartaruga.pensize(2)
tartaruga.pencolor("black")


tela = turtle.Screen()
tela.bgpic("teste_ia.gif")
turtle.onscreenclick(get_mouse_click_coor)
turtle.listen()
turtle.onkey(space, 'space')
turtle.onkey(space, 'Return')
turtle.onkey(branco, 'b')
turtle.onkey(preto, 'p')

turtle.mainloop()
