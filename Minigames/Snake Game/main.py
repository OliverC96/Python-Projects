# Importing relevant classes/modules
from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

high_score = 0


# Initiates a game of snake
def play_snake():

    # Creating the snake, food, and scoreboard objects (all derived from the Turtle class)
    global high_score
    game_on = True
    snake = Snake("square", "white")
    food = Food()
    scoreboard = Scoreboard(high_score)

    # Creating and formatting the screen object
    screen = Screen()
    screen.setup(600, 600)
    screen.bgcolor("black")
    screen.title("Snake Game")
    screen.tracer(0)
    screen.listen()

    # Pairing the snake's movement methods with the arrow keys using key event listeners
    screen.onkey(snake.move_up, "Up")
    screen.onkey(snake.move_down, "Down")
    screen.onkey(snake.move_right, "Right")
    screen.onkey(snake.move_left, "Left")

    # Continues looping until either the snake collides with a wall, or with any part of its own tail
    while game_on:

        # Updates the screen, and moves the snake on each iteration of the while loop
        screen.update()
        time.sleep(0.1)
        snake.move()

        # Handling the case in which the snake eats (i.e. 'collides with') the food object
        if snake.head.distance(food) < 15:

            food.refresh()
            scoreboard.increase_score()
            snake.grow()

        if snake.wall_collision() or snake.tail_collision():

            game_on = False

    # Updating the global high score variable and resetting the screen, in preparation for future games
    high_score = scoreboard.high_score
    screen.clearscreen()

if __name__ == '__main__':

    # Welcome message and game instructions
    print('Welcome to Snake Game!')
    print('- Use the arrow keys to move around')
    print('- Eat food to grow your snake')
    print('- Avoid colliding with the walls')
    print('- Avoid colliding with your tail')

    choice = input('Play (P) or Quit (Q)? ')

    while choice not in ['P', 'p', 'Q', 'q']:

        choice = input('Invalid choice - Play (P) or Quit (Q)? ')

    while choice.lower() != 'q':

        play_snake()

        choice = input('Play (P) or Quit (Q)? ')

        while choice not in ['P', 'p', 'Q', 'q']:

            choice = input('Invalid choice - Play (P) or Quit (Q)? ')

    # Closing message
    print('Your high score was {}!'.format(high_score))
    print('Thanks for playing!')
    high_score = 0
