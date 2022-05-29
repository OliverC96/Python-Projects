from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self):

        super().__init__()
        self.shape("circle")
        self.color("blue")
        self.penup()
        self.shapesize(0.5, 0.5)
        self.speed("fastest")
        self.refresh()

    def refresh(self):

        self.setpos(random.randint(-260,260), random.randint(-260,240))


