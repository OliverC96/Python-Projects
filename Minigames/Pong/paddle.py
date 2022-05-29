from turtle import Turtle


class Paddle(Turtle):

    def __init__(self, player):

        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.reverse = False

        if player == 'comp':

            self.setpos(-370, 0)
            self.shapesize(14,1)

        else:

            self.setpos(360, 0)
            self.shapesize(6, 1)

    def move(self):

        all_y = [y for y in range(-261, 261) if y % 40 == 0]

        curr_index = all_y.index(int(self.ycor()))

        if not self.reverse:

            if curr_index == len(all_y) - 1:

                self.setpos(self.xcor(), all_y[curr_index - 1])
                self.reverse = True

            else:

                self.setpos(self.xcor(), all_y[curr_index + 1])

        else:

            if curr_index == 0:

                self.setpos(self.xcor(), all_y[curr_index + 1])
                self.reverse = False

            else:

                self.setpos(self.xcor(), all_y[curr_index - 1])

    def move_up(self):

        if self.ycor() < 240:

            new_y = self.ycor() + 40
            curr_x = self.xcor()
            self.setpos(curr_x, new_y)

    def move_down(self):

        if self.ycor() > -240:

            new_y = self.ycor() - 40
            curr_x = self.xcor()
            self.setpos(curr_x, new_y)
