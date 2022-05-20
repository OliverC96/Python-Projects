import random

# Constructing relevant global variables
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
          'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}


# Represents a single card
class Card:

    # Initializes the Card's attributes
    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    # String representation of the Card object
    def __str__(self):

        return '{} of {}'.format(self.rank, self.suit)


# Represents a 52-card game deck
class Deck:

    # Initializes the Deck's attributes
    def __init__(self):

        self.all_cards = []

        for suit in suits:

            for rank in ranks:

                self.all_cards.append(Card(suit, rank))

    # Pseudo-randomly shuffles the deck
    def shuffle(self):

        random.shuffle(self.all_cards)

    # Deals the top card off the deck
    def deal_one(self):

        return self.all_cards.pop()

    # String representation of the entire deck (list of Card objects)
    def __str__(self):

        deck_string = ''

        for card in self.all_cards:

            deck_string += card.__str__() + '\n'

        return deck_string


# Represents a player's hand in the game of Blackjack
class Hand:

    # Initializes the attributes of the Hand object
    def __init__(self):

        self.cards = []
        self.value = 0
        self.aces = 0

    # Adds a new card to the hand, and updates the total value accordingly
    def add_card(self, new_card):

        self.cards.append(new_card)
        self.value += values[new_card.rank]

        if new_card.rank == 'Ace':

            self.aces += 1

    # Adjusts the value of aces in accordance with the rules of Blackjack
    def ace_adjustment(self):

        while self.value > 21 and self.aces > 0:

            self.value -= 10
            self.aces -= 1


# Represents a player's bankroll/balance in a game of Blackjack
class Chips:

    # Initializes appropriate attributes
    def __init__(self, initial_deposit=0):

        self.total = initial_deposit
        self.bet = 0

    # Increases the total amount of chips (by the bet amount) in the case that the player wins the round
    def win_bet(self):

        self.total += self.bet

    # Decreases the total amount of chips (by the bet amount) in the case that the player loses the round
    def lose_bet(self):

        self.total -= self.bet


# Prompts the player to place a bet, and ensures that the bet is a valid amount
def take_bet(chips):

    while True:

        try:

            chips.bet = int(input('How many chips would you like to bet? '))

        except ValueError:

            print('Sorry, the bet must be an integer value')

        else:

            if chips.bet > chips.total:

                print("Sorry, your bet can't exceed {} chips".format(chips.total))

            else:

                break


# Handles the scenario in which one chooses to hit (gain another card from the deck)
def hit(deck, hand):

    single_card = deck.deal_one()
    hand.add_card(single_card)
    hand.ace_adjustment()


# Prompts the player to hit or stand, and proceeds accordingly
def hit_or_stand(deck, hand):

    game_on = True
    user_choice = input("\nEnter 'h' to hit; 's' to stand: ")

    while user_choice not in ['H', 'h', 'S', 's']:

        user_choice = input("Invalid choice, enter 'h' to hit; 's' to stand: ")

    if user_choice.lower() == 'h':

        hit(deck, hand)

    else:

        print('Player stands - dealer is playing')
        game_on = False

    return game_on


# Displays one of the dealer's cards, and all of the player's cards
def show_some(dealer, player):

    print("\nDealer's hand:")
    print('HIDDEN')
    print(dealer.cards[1])

    print("\nPlayer's hand:")

    for card in player.cards:

        print(card)

    print("Total value: {}".format(player.value))


# Displays all of the dealer's cards, and all of the player's cards
def show_all(dealer, player):

    print("\nDealer's hand:")

    for card in dealer.cards:

        print(card)

    print("Total value: {}".format(dealer.value))

    print("\nPlayer's hand:")

    for card in player.cards:

        print(card)

    print("Total value: {}".format(player.value))


# Handles the scenario in which the player busts (exceeds 21)
def player_busts(chips):

    print('\nPLAYER BUSTS')
    chips.lose_bet()


# Handles the scenario in which the player wins
def player_wins(chips):

    print('\nPLAYER WINS')
    chips.win_bet()


# Handles the scenario in which the dealer busts (exceeds 21)
def dealer_busts(chips):

    print('\nDEALER BUSTS - PLAYER WINS')
    chips.win_bet()


# Handles the scenario in which the dealer wins
def dealer_wins(chips):

    print('\nDEALER WINS')
    chips.lose_bet()


# Handles the occurrance of a push (neither the dealer nor the player wins)
def push():

    print('\nPLAYER AND DEALER TIE - PUSH')
