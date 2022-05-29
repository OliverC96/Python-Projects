# Importing relevant classes/modules
from turtle import Screen
from paddle import Paddle
from ball import Ball
from pong_score import PongScore
import time


# Initiates a game of pong
def play_pong():

    # Creating the two paddles, the ball, and the scoreboard
    user_paddle = Paddle("user")
    comp_paddle = Paddle("comp")
    ball = Ball()
    scoreboard = PongScore()

    # Creating and formatting the screen object
    screen = Screen()
    screen.setup(800, 610)
    screen.bgcolor("black")
    screen.title("Pong")
    screen.tracer(0)
    screen.listen()
    screen.onkey(user_paddle.move_up, "Up")
    screen.onkey(user_paddle.move_down, "Down")
    game_on = True

    # Loop continues until one of the players has reached a score of 7
    while game_on:

        # Updates the screen and moves the paddles and ball on each iteration of the while loop
        time.sleep(ball.move_speed)
        screen.update()
        comp_paddle.move()
        ball.move()

        # Reversing the vertical direction of the ball if it collides with either the top or bottom wall
        if ball.ycor() > 285 or ball.ycor() < -275:

            ball.bounce_y()

        # Reversing the horizontal direction of the ball if it collides with either paddle
        if (user_paddle.distance(ball) < 65 and ball.xcor() > 330) or (comp_paddle.distance(ball) < 180 and ball.xcor() < -350):

            ball.bounce_x()

        # User wins the round - increments their score, and resets the ball's position (to (0,0))
        if ball.xcor() < -375:

            scoreboard.increase_score("user")
            ball.reset_position()

        # Computer wins the round - increments their score, and resets the ball's position
        if ball.xcor() > 370:

            scoreboard.increase_score("comp")
            ball.reset_position()

        if scoreboard.c_points == 7:

            print('You lost - better luck next time!')
            game_on = False

        if scoreboard.p_points == 7:

            print('You won - good job!')
            game_on = False


if __name__ == '__main__':

    # Welcome message and game instructions
    print('Welcome to Pong!')
    print('- Use arrow keys to move paddle up or down')
    print('- First to 7 wins - good luck!')

    choice = input('Play (P) or Quit (Q)? ')

    while choice not in ['P', 'p', 'Q', 'q']:

        choice = input('Invalid choice - Play (P) or Quit (Q)? ')

    while choice.lower() != 'q':

        play_pong()

        choice = input('Play (P) or Quit (Q)? ')

        while choice not in ['P', 'p', 'Q', 'q']:

            choice = input('Invalid choice - Play (P) or Quit (Q)? ')

    # Closing message
    print('Thanks for playing!')

