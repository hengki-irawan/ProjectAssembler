from turtle import Turtle, Screen
import random as r
import color_palette as cp

class DrawingFunctions:
    def __init__(self, cursor):
        self.cursor = cursor

    def spirograph(self, gap_size):
        self.cursor.penup()
        self.cursor.goto(160, -150)
        self.cursor.pendown()
        for _ in range(int(360 / gap_size)):
            self.cursor.color(r.choice(cp.pallet_b))
            self.cursor.circle(70)
            self.cursor.setheading(self.cursor.heading() + gap_size)

    def rectangle(self, x, y):
        self.cursor.goto(x, y)
        self.cursor.setheading(45)
        self.cursor.forward(15)
        self.cursor.setheading(0)

        number_of_dots = 144

        for dot_count in range(1, number_of_dots + 1):
            self.cursor.dot(20, r.choice(cp.pallet_a))
            self.cursor.forward(25)  # a

            if dot_count % 12 == 0:  # b
                self.cursor.setheading(90)
                self.cursor.forward(25)
                self.cursor.setheading(180)
                self.cursor.forward(300)  # a*b
                self.cursor.setheading(0)

    def stars(self, gap_size):
        self.cursor.penup()
        self.cursor.goto(-280, 200)
        self.cursor.pendown()

        for _ in range(int(360 / gap_size)):
            self.cursor.color(r.choice(cp.pallet_b))
            self.cursor.forward(250)
            self.cursor.right(150)
            self.cursor.setheading(self.cursor.heading() + gap_size)


