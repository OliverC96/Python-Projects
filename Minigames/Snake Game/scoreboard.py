from turtle import Turtle


class Scoreboard(Turtle):

    def __init__(self, high_score):

        super().__init__()
        self.score = 0
        self.high_score = high_score
        self.color("white")
        self.penup()
        self.setpos(0, 260)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):

        if self.score > self.high_score:

            self.high_score = self.score

        self.write("Current Score: {} | High Score: {}".format(self.score, self.high_score), align="center", font=("Arial", 24, "normal"))

    def increase_score(self):

        self.score += 1
        self.clear()
        self.update_scoreboard()
