from turtle import Turtle
import random


class Ball(Turtle):

    def __init__(self):

        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.y_move = 10
        self.x_move = 10
        self.move_speed = 0.04

    def move(self):

        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.setpos(new_x, new_y)

    def bounce_y(self):

        self.y_move *= -1

    def bounce_x(self):

        self.x_move *= -1
        self.move_speed *= 0.9

    def reset_position(self):

        self.setpos(0, 0)
        self.move_speed = 0.04
        rand_num = random.randint(0, 1)

        if rand_num == 0:

            self.x_move = 10
            self.y_move = 10

        else:

            self.x_move = 10
            self.y_move = -10
