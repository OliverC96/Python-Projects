from blackjack_setup import *

# Initiates a game of blackjack between a human player and a computer dealer
def play_blackjack(amount):

    # Creates and shuffles the game deck
    game_deck = Deck()
    game_deck.shuffle()
    player_chips = Chips(amount)
    game_on = True

    # Displays player's balance, and gives them the option to purchase additional chips before heading into the next round
    print('Your current balance is: {} chips'.format(player_chips.total))
    user_chips = input("Enter 'p' to purchase additional chips; 'c' to continue ")

    while user_chips not in ['P', 'p', 'C', 'c']:

        user_chips = input("Please enter a valid option - p or c: ")

    if user_chips.lower() == 'p':

        top_up = input("How many chips would you like to purchase? ")

        while not top_up.isdigit():

            top_up = input("Please enter a valid integer amount: ")

        player_chips.total += int(top_up)
        print('Your updated balance is: {} chips'.format(player_chips.total))

    # Takes the player's bet, and deals two cards to both the player and the dealer
    take_bet(player_chips)
    player_hand = Hand()
    dealer_hand = Hand()

    for i in range(2):

        player_hand.add_card(game_deck.deal_one())
        dealer_hand.add_card(game_deck.deal_one())

    # Displays one of the dealer's card, and both of the player's cards
    show_some(dealer_hand, player_hand)

    while game_on:

        # Prompts the player to hit or stand, and displays their updated hand
        game_on = hit_or_stand(game_deck, player_hand)
        show_some(dealer_hand, player_hand)

        # Player busts; round is over
        if player_hand.value > 21:

            player_busts(player_chips)
            game_on = False

    # Player stands; dealer's turn
    if player_hand.value <= 21:

        # Dealer hits until their hand exceeds that of the player's
        while dealer_hand.value < player_hand.value:

            hit(game_deck, dealer_hand)

        # Displays both the dealer's and player's hands
        show_all(dealer_hand, player_hand)

        # Dealer busts; round is over
        if dealer_hand.value > 21:

            dealer_busts(player_chips)

        # Player wins; round is over
        elif player_hand.value > dealer_hand.value:

            player_wins(player_chips)

        # Dealer wins; round is over
        elif player_hand.value < dealer_hand.value:

            dealer_wins(player_chips)

        # Dealer and player tie; round is over
        else:

            push()

    # Displays the player's updated chip balance
    print('Your updated total is: {} chips'.format(player_chips.total))
    global player_balance
    player_balance = player_chips.total


if __name__ == "__main__":

    # Welcome message
    print('Welcome to Blackjack!')

    user_choice = input("Enter 'p' to play; 'q' to quit: ")

    while user_choice not in ['P', 'p', 'Q', 'q']:

        user_choice = input('Please enter a valid option - p or q: ')

    player_balance = 0

    # Continually progresses onto the next round of Blackjack until the player wishes to quit the program
    while user_choice.lower() != 'q':

        play_blackjack(player_balance)
        user_choice = input("Enter 'p' to play; 'q' to quit: ")

    # Closing message
    print('Thank you for playing Blackjack!')
