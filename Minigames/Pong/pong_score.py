from turtle import Turtle


class PongScore(Turtle):

    def __init__(self):

        super().__init__()
        self.p_points = 0
        self.c_points = 0
        self.color("white")
        self.penup()
        self.setpos(0, 230)
        self.update_scoreboard()
        self.create_divider()

    def update_scoreboard(self):

        self.write("{}      {}".format(self.c_points, self.p_points), align="center", font=("Arial", 50, "normal"))

    def increase_score(self, player):

        if player == 'user':

            self.p_points += 1

        else:

            self.c_points += 1

        self.clear()
        self.update_scoreboard()

    def create_divider(self):

        y_positions = [y for y in range(-280, 320) if y % 40 == 0]

        for i in range(len(y_positions)):

            s = Turtle("square")
            s.penup()
            s.color("white")
            s.shapesize(0.5, 0.25)
            s.setpos(0, y_positions[i])
