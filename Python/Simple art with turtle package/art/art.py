from turtle import Turtle, Screen
from shapes import DrawingFunctions

if __name__ == "__main__":
    cursor = Turtle()
    screen = Screen()
    screen.title('Lines and Dots Art')
    screen.screensize(600, 600)
    screen.colormode(255)
    screen.bgcolor((227, 220, 196))
    cursor.hideturtle()
    cursor.speed('fastest')

    drawing = DrawingFunctions(cursor)

    drawing.spirograph(5)
    cursor.penup()
    drawing.rectangle(10, 10)
    cursor.pendown()
    drawing.stars(8)
    cursor.penup()
    drawing.rectangle(-300, -290)

    screen.exitonclick()