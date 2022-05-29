import random

# Declaring and initializing the global game board
game_board = ['#', '', '', '', '', '', '', '', '', '']


# Determines whether or not the game board is full
def full_board():

    for element in game_board[1:]:
        if element == '':
            return False

    return True


# Updates the game board, by placing the player's marker on their desired position
def update_board(marker, player):

    position = int(input('{}, please choose an available position to place your marker on [{}]: '.format(player, marker)))
    while position not in range(1, 11) or game_board[position] != '':
        position = int(input('Please enter a valid position: '))
    game_board[position] = marker
    print_board()


# Prints out a visual representation of the game board
def print_board():

    print('{:^3}|{:^3}|{:^3}'.format(game_board[1], game_board[2], game_board[3]))
    print('-----------')
    print('{:^3}|{:^3}|{:^3}'.format(game_board[4], game_board[5], game_board[6]))
    print('-----------')
    print('{:^3}|{:^3}|{:^3}'.format(game_board[7], game_board[8], game_board[9]))


# Determines whether or not a player has won the game (searches for 3-consecutive-slot streaks of their marker)
def win_check(marker):

    winning_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 5, 9], [3, 5, 7], [1, 4, 7], [2, 5, 8], [3, 6, 9]]
    positions = []
    pos = 1

    for element in game_board[1:]:

        if element == marker:
            positions.append(pos)
        pos += 1

    for combo in winning_combinations:

        if set(combo).intersection(set(positions)) == set(combo):
            return True

    return False


# Clears the game board in preparation for a new game
def reset_board():

    i = 1
    while i < len(game_board):
        game_board[i] = ''
        i += 1


# Initiates a game of Tic-Tac-Toe between two players on a single computer interface
def play_game():

    p1_marker = input('Player 1, please choose a marker: X or O ')
    while p1_marker != 'X' and p1_marker != 'O':
        p1_marker = input('Please choose a valid marker: X or O ')
    if p1_marker.upper() == 'X':
        p2_marker = 'O'
    else:
        p2_marker = 'X'

    starter = random.randint(1,2)

    if starter == 1:
        print('Player 1 will go first!')
        print_board()
        update_board(p1_marker, 'Player 1')
    else:
        print('Player 2 will go first!')
        print_board()
        update_board(p2_marker, 'Player 2')

    game_over = False

    # Continually progresses to the next step until either a player has won, or the game board is full (whichever is first)
    while not game_over and not full_board():

        if starter == 1:

            update_board(p2_marker, 'Player 2')
            p2_winner = win_check(p2_marker)
            if p2_winner:
                print('Player 2 Wins!')
                game_over = True
                break

            update_board(p1_marker, 'Player 1')
            p1_winner = win_check(p1_marker)
            if p1_winner:
                print('Player 1 Wins!')
                game_over = True
                break

        else:

            update_board(p1_marker, 'Player 1')
            p1_winner = win_check(p1_marker)
            if p1_winner:
                print('Player 1 Wins!')
                game_over = True
                break

            update_board(p2_marker, 'Player 2')
            p2_winner = win_check(p2_marker)
            if p2_winner:
                print('Player 2 Wins!')
                game_over = True
                break

    # A tie game results if the game board is full, but there is no winner
    if not game_over and full_board():

        print('Tie Game!')

    reset_board()

# Welcome message
print('Welcome to Tic-Tac-Toe!')
user_choice = input("Enter 'p' to play; 'q' to quit: ")

# Continually initiates new games of Tic-Tac-Toe until the user chooses to quit (sentinel value of 'q' is entered)
while user_choice.lower() != 'q':

    play_game()
    user_choice = input("Enter 'p' to play; 'q' to quit: ")

# Closing message
print('Thanks for playing!')
