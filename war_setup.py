import random

# Constructing relevant global variables for a deck of cards
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
          'Nine':9, 'Ten':10, 'Jack':11, 'Queen':12, 'King':13, 'Ace':14}


# Objects of this class represent a single card in the game of war
class Card:

    # Initializing instance variables
    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    # String representation of the card
    def __str__(self):

        return '{} of {}'.format(self.rank, self.suit)


# Objects of this class represent a deck of cards (list of Card objects)
class Deck:

    # Initializing instance variables
    def __init__(self):

        self.all_cards = []

        for suit in suits:

            for rank in ranks:

                self.all_cards.append(Card(suit, rank))

    # Pseudo-randomly shuffles/rearranges the deck of cards
    def shuffle(self):

        random.shuffle(self.all_cards)

    # Returns a single card (from the top of the deck)
    def deal_one(self):

        return self.all_cards.pop()


# Objects of this class represent different players in the war game
class Player:

    # Initializing instance variables
    def __init__(self, name):

        self.name = name
        self.all_cards = []

    # Removes and retrieves the first card (from the bottom of the deck)
    def remove_one(self):

        return self.all_cards.pop(0)

    # Adds card(s) to the player's current deck
    def add_cards(self, new_cards):

        if type(new_cards) == type([]):

            self.all_cards.extend(new_cards)

        else:

            self.all_cards.append(new_cards)

    # String representation of the player and their cards
    def __str__(self):

        return 'Player {} has {} cards'.format(self.name, len(self.all_cards))

