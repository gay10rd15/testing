import turtle

window = turtle.Screen()
window.bgcolor("white")
T = turtle.Turtle()
T.speed(100)


def A(turtle: turtle.Turtle):
    turtle.forward(100)
    turtle.rt(3)
    turtle.bk(99)


for i in range(360):
    A(T)

window.exitonclick()
