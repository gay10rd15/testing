import turtle

window = turtle.Screen()
window.bgcolor("white")
T = turtle.Turtle()
T.speed(3)
for i in range(20):
    T.forward(2**i / 2)
    T.left(90)

window.exitonclick()
