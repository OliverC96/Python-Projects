from turtle import Turtle

STARTING_POSITIONS = [(0,0), (-20, 0), (-40, 0)]
MOVE_DISTANCE = 20
UP = 90
DOWN = 270
RIGHT = 0
LEFT = 180


class Snake(Turtle):

    def __init__(self, shape, colour):

        super().__init__()
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):

        for i in range(3):

          s = Turtle("square")
          s.penup()
          s.color("white")
          s.setpos(STARTING_POSITIONS[i])
          self.segments.append(s)

    def move(self):

        for seg_num in range(len(self.segments) - 1, 0, -1):

            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].setpos(new_x, new_y)

        self.head.forward(MOVE_DISTANCE)

    def move_up(self):

        if self.head.heading() not in [UP, DOWN]:

            self.head.setheading(UP)

    def move_down(self):

        if self.head.heading() not in [UP, DOWN]:

            self.head.setheading(DOWN)

    def move_right(self):

        if self.head.heading() not in [RIGHT, LEFT]:

            self.head.setheading(RIGHT)

    def move_left(self):

        if self.head.heading() not in [RIGHT, LEFT]:

            self.head.setheading(LEFT)

    def wall_collision(self):

        return self.head.xcor() < -300 or self.head.xcor() > 300 or self.head.ycor() < -300 or self.head.ycor() > 300

    def tail_collision(self):

        for segment in self.segments[1:]:

            if self.head.distance(segment) < 15:

                return True

        return False

    def grow(self):

        for _ in range(2):

            s = Turtle("square")
            s.color("white")
            s.penup()
            self.segments.append(s)
