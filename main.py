import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playername = input("Enter your player name: ")

playing = True

# CLASSES
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def surrender(self, chips):
        chips.total -= chips.bet // 2
        print("Player surrenders. Half of the bet is returned.")

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def split_hand(self):
        card = self.cards.pop()
        new_hand = Hand()
        new_hand.add_card(card)
        return new_hand

class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def display_chips(chips):
    print(f"\nWelcome {playername}! You currently have {chips.total} chips.")

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Sorry! Please can you type in a number: ")
        else:
            if chips.bet > chips.total:
                print("You bet can't exceed your total chips!")
            else:
                break

def play_hand(deck, hand):
    while True:
        ask = input("\nWould you like to [h]it or [s]tand? ")
        if ask[0].lower() == 'h':
            hit(deck, hand)
            if hand.value > 21:
                print("Bust!")
                break
        elif ask[0].lower() == 's':
            print("Stand.")
            break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing
    while True:
        ask = input("\nWould you like to [h]it, [s]tand, or [u]surrender? ")
        if ask[0].lower() == 'h':
            hit(deck, hand)
        elif ask[0].lower() == 's':
            print("Player stands, Dealer is playing.")
            playing = False
        elif ask[0].lower() == 'u':
            hand.surrender(player_chips)
            playing = False
        else:
            print("Sorry! I did not understand that! Please try again!")
            continue
        break

def show_some(player, dealer):
    print("\nDealer's Hand: ")
    print(" <card hidden>")
    print("", dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand: ", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

def player_busts(player, dealer, chips):
    print("PLAYER BUSTS!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    if player.value == 21 and len(player.cards) == 2:
        print("PLAYER BLACKJACK!")
        chips.win_bet()
    else:
        print("PLAYER WINS!")
        chips.win_bet()
    print(f"Player's Chips: {chips.total}")

def dealer_busts(player, dealer, chips):
    print("DEALER BUSTS!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    if dealer.value == 21 and len(dealer.cards) == 2:
        print("DEALER BLACKJACK!")
        chips.lose_bet()
    else:
        print("DEALER WINS!")
        chips.lose_bet()
    print(f"Player's Chips: {chips.total}")

def push(player, dealer):
    print("Its a push! Player and Dealer tie!")

class GameStats:
    def __init__(self):
        self.games_played = 0
        self.player_wins = 0
        self.dealer_wins = 0
        self.pushes = 0
        self.player_blackjacks = 0
        self.dealer_blackjacks = 0

    def update_stats(self, result):
        self.games_played += 1
        if result == 'player':
            self.player_wins += 1
        elif result == 'dealer':
            self.dealer_wins += 1
        elif result == 'push':
            self.pushes += 1
        elif result == 'player_blackjack':
            self.player_blackjacks += 1
        elif result == 'dealer_blackjack':
            self.dealer_blackjacks += 1

    def display_stats(self):
        print("\nGame Statistics:")
        print(f"Games Played: {self.games_played}")
        print(f"Player Wins: {self.player_wins}")
        print(f"Dealer Wins: {self.dealer_wins}")
        print(f"Pushes: {self.pushes}")
        print(f"Player Blackjacks: {self.player_blackjacks}")
        print(f"Dealer Blackjacks: {self.dealer_blackjacks}")

game_stats = GameStats()


def reset_hands(deck, player_hand, dealer_hand):
    player_hand.cards = []
    dealer_hand.cards = []
    player_hand.value = 0
    dealer_hand.value = 0
    player_hand.aces = 0
    dealer_hand.aces = 0
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

def continue_playing():
    while True:
        choice = input("\nWould you like to continue playing? Enter 'y' to continue or 'n' to quit: ")
        if choice.lower() in ['y', 'n']:
            return choice.lower() == 'y'
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")

# Gameplay!
while True:
    print("Welcome to BlackJack!")

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    player_chips = Chips()

    display_chips(player_chips)

    while player_chips.total > 0:
        take_bet(player_chips)

        reset_hands(deck, player_hand, dealer_hand)

        show_some(player_hand, dealer_hand)

        playing = True
        while playing:
            hit_or_stand(deck, player_hand)
            show_some(player_hand, dealer_hand)

            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                game_stats.update_stats('dealer')
                break

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
                game_stats.update_stats('player')
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
                game_stats.update_stats('dealer')
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
                game_stats.update_stats('player')
            elif player_hand.value == dealer_hand.value:
                push(player_hand, dealer_hand)
                game_stats.update_stats('push')

        game_stats.display_stats()
        print("\nPlayer's remaining chips: ", player_chips.total)

        if player_chips.total == 0:
            print("\nYou've run out of chips!")
            if not continue_playing():
                print("\nThanks for playing!")
                break
        else:
            while True:
                new_game = input("\nWould you like to play again? Enter 'y' or 'n': ")
                if new_game[0].lower() == 'y':
                    print("Current Chips: ", player_chips.total)
                    break
                elif new_game[0].lower() == 'n':
                    print("\nThanks for playing!")
                    exit()  # Terminate the game
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
