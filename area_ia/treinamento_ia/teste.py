# como usar: fazer o traço e depois definir se é branco ou preto o preenchimento
# dar enter ou espaço para sair

import turtle
from tkinter import PhotoImage
from PIL import Image


HOSPITAL = 33


def get_mouse_click_coor(x, y):
    print(x, y)
    tartaruga.setpos(x, y)
    pontos.append((x, y))
    tartaruga.pendown()


def space():
    global HOSPITAL
    tartaruga.pensize(0)
    tartaruga.speed(0)
    tartaruga.shape('blank')
    tartaruga.up()
    tartaruga.goto(-largura/2, -altura/2)
    tartaruga.pendown()
    tartaruga.fillcolor("black")
    tartaruga.begin_fill()
    tartaruga.goto(-largura/2, altura/2)
    tartaruga.goto(largura/2, altura/2)
    tartaruga.goto(largura/2, -altura/2)
    tartaruga.goto(-largura/2, -altura/2)
    tartaruga.end_fill()
    tartaruga.penup()

    for i in range(len(poligonos)):
        tartaruga.goto(poligonos[i][0][0], poligonos[i][0][1])
        tartaruga.begin_fill()
        if cor[i] == 1:
            tartaruga.fillcolor("white")
        else:
            tartaruga.fillcolor("black")

        for j in range(1, len(poligonos[i])):
            tartaruga.goto(poligonos[i][j][0], poligonos[i][j][1])
            tartaruga.pendown()
        tartaruga.penup()
        tartaruga.end_fill()

    tartaruga.screen.getcanvas().postscript(file=f"img_eps/map{HOSPITAL}.eps")

    imagem = Image.open(f"img_eps/map{HOSPITAL}.eps")
    imagem = imagem.resize((250, 250))
    imagem.save(f"img_cont_png/map{HOSPITAL}.png")


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

largura, altura = 1000, 1000
screen = turtle.Screen()
screen.setup(largura, altura)
larger = PhotoImage(file="img_trein/map33.gif").zoom(4, 4)
screen.addshape("img", turtle.Shape("image", larger))

t1 = turtle.Turtle("img")

tartaruga = turtle.Turtle()

tartaruga.penup()
tartaruga.pensize(2)
tartaruga.shape('blank')
tartaruga.pencolor("black")


# tela = turtle.Screen()
# imagem = PhotoImage(file="img_trein/map11.gif")
# # tela.bgpic("img_trein/map11.gif")
# tela.bgpic(imagem)

turtle.onscreenclick(get_mouse_click_coor)
turtle.listen()
turtle.onkey(space, 'space')
turtle.onkey(space, 'Return')
turtle.onkey(branco, 'b')
turtle.onkey(preto, 'p')

turtle.mainloop()
