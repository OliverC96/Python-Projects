from war_setup import *


# Initiates a game of war
def play_war():

    # Instantiating two distinct players and a shuffled deck of cards
    p1 = Player("One")
    p2 = Player("Two")
    game_deck = Deck()
    game_deck.shuffle()

    # Dealing the 52 cards evenly between the two players (in alternating order)
    for x in range(26):

        p1.add_cards(game_deck.deal_one())
        p2.add_cards(game_deck.deal_one())

    game_on = True
    round_num = 0

    # Continually progresses to the next round until game_on = False (sentinel value)
    while game_on:

        # Increments, and outputs the round number
        round_num += 1
        print('Round {}'.format(round_num))

        # If player one has no cards left, they are unable to continue, and player two wins
        if len(p1.all_cards) == 0:

            print('Player One out of cards - game over!')
            print('Player Two wins!')
            game_on = False
            break

        # If player two has no cards left, they are unable to continue, and player one wins
        if len(p2.all_cards) == 0:

            print('Player Two out of cards - game over!')
            print('Player One wins!')
            game_on = False
            break

        # Moves one card from each player's deck, and pits them up against each other in war
        p1_cards = [p1.remove_one()]
        p2_cards = [p2.remove_one()]
        at_war = True

        # Continually initiates war until at_war = False (sentinel value)
        while at_war:

            # If player one's card is greater in value than player two's card, they win the war, and collect player two's card
            if p1_cards[-1].value > p2_cards[-1].value:

                p1.add_cards(p1_cards)
                p1.add_cards(p2_cards)
                at_war = False

            # If player two's card is greater in value than player one's card, they win the war, and collect player one's card
            elif p1_cards[-1].value < p2_cards[-1].value:

                p2.add_cards(p2_cards)
                p2.add_cards(p1_cards)
                at_war = False

            # Executes if player one's card and player two's card are equal in value
            else:

                print('War!')

                # Player one has less than 5 cards left, so the war is over and player two wins
                if len(p1.all_cards) < 5:

                    print('Player One unable to declare war - Player Two wins!')
                    game_on = False
                    break

                # Player two has less than 5 cards left, so the war is over and player one wins
                elif len(p2.all_cards) < 5:

                    print('Player Two unable to declare war - Player One wins!')
                    game_on = False
                    break

                # Otherwise, further cards are drawn, and the war continues
                else:

                    for num in range(5):

                        p1_cards.append(p1.remove_one())
                        p2_cards.append(p2.remove_one())


# Executes if the __name__ keyword is set to "__main__" (the module is not imported)
if __name__ == "__main__":

    # Initiates another game of war, or terminates the program depending on the user's input
    choice = input("Welcome to War! Enter 'p' to play; 'q' to quit: ")
    while choice not in ['P', 'p', 'Q', 'q']:
        choice = input('Please enter a valid choice - p or q: ')

    while choice.lower() != 'q':

        play_war()
        choice = input("Welcome to War! Enter 'p' to play; 'q' to quit: ")
        while choice not in ['P', 'p', 'Q', 'q']:
            choice = input('Please enter a valid choice - p or q: ')

    # Outputs closing message
    print('Thank you for playing war!')
