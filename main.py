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
    def __init__(self, num_decks=1):
        self.deck = []
        self.num_decks = num_decks
        self.create_deck()
        self.shuffle()

    def create_deck(self):
        for _ in range(self.num_decks):
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

class NPCPlayer:
    def __init__(self, name, chips=100):
        self.name = name
        self.chips = chips

    def take_bet(self):
        bet_amount = random.randint(0, 500)
        if bet_amount > self.chips:
            bet_amount = self.chips
        return bet_amount

    def make_decision(self, player_hand):
        while self.get_hand_value(player_hand) < 17:
            return 'hit'
        return 'stand'

    def get_hand_value(self, hand):
        hand_value = sum(values[card.rank] for card in hand.cards)
        return hand_value

def dealer_play(deck, dealer_hand):
    while dealer_hand.value < 17:
        hit(deck, dealer_hand)
        if dealer_hand.value > 21:
            print("Dealer BUSTS!")
            game_stats.update_stats('player')
            return 'bust'
    if dealer_hand.value == 17:
        print("Dealer stands.")
        return 'stand'
    else:
        return 'hit'

def npc_play(deck, npc_hand):
    while npc_hand.value < 17:
        hit(deck, npc_hand)
        if npc_hand.value > 21:
            print("NPC BUSTS!")
            game_stats.update_stats('player', 'npc')
            return 'bust'
    if npc_hand.value == 17:
        print("NPC stands.")
        return 'stand'
    else:
        return 'hit'

def display_chips():
    while True:
        try:
            chips = int(input("Enter how many chips you want to play with: "))
            if chips <= 0:
                print("Please enter a positive number of chips.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"\nWelcome {playername}! You currently have {chips} chips.")
    return chips

def take_bet(chips):
    while True:
        try:
            bet_option = int(input("How many chips would you like to bet? "))
            if bet_option <= 0:
                print("Please enter a positive bet amount.")
                continue
            if bet_option > chips.total:
                print("You can't bet more than your total chips!")
                continue
            chips.bet = bet_option
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        double_down_option = input("Would you like to double down? [y/n] ")
        if double_down_option.lower() == 'y':
            if chips.total >= chips.bet * 2:
                chips.bet *= 2
                print("You chose to double down.")
                break
            else:
                print("Insufficient chips to double down.")
                retry_option = input("Would you like to enter another bet amount? [y/n] ")
                if retry_option.lower() == 'y':
                    while True:
                        try:
                            new_bet = int(input("Enter a different bet amount: "))
                            if new_bet > chips.total:
                                print("You can't bet more than your total chips!")
                                continue
                            chips.bet = new_bet * 2
                            print("You chose to double down with a different bet amount.")
                            break
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                    break
                elif retry_option.lower() == 'n':
                    break
                else:
                    print("Please enter 'y' or 'n' for your choice.")
        elif double_down_option.lower() == 'n':
            break
        else:
            print("Please enter 'y' or 'n' for your choice.")


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

def hit_or_stand(deck, hand, dealer=False):
    global playing
    while True:
        if dealer:
            if hand.value >= 17:
                print("Dealer stands.")
                playing = False
                break
            else:
                hit(deck, hand)
                print("Dealer hits.")
                print(f"Dealer's Hand: {hand.value}")
        else:
            ask = input("\nWould you like to [h]it, [s]tand, or [u]surrender? ")
            if ask[0].lower() == 'h':
                hit(deck, hand)
                print("Player hits.")
            elif ask[0].lower() == 's':
                print("Player stands.")
                playing = False
            elif ask[0].lower() == 'u':
                hand.surrender(player_chips)
                playing = False
            elif ask[0].lower() == 'd':
                if player_chips.total >= player_chips.bet * 2:
                    print("You chose to double down.")
                    player_chips.bet *= 2
                    hit(deck, hand)
                    playing = False
                else:
                    print("Insufficient chips to double down.")
            else:
                print("Sorry! I did not understand that! Please try again!")
                continue
        break



def show_some(player, dealer, npc):
    print("\nDealer's Hand: ")
    print(" <card hidden>")
    print("", dealer.cards[1])
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print("\nNPC's Hand: ", *npc.cards, sep='\n ')

def show_all(player, dealer, npc):
    print("\nDealer's Hand: ", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand: ", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)
    print("\nNPC's Hand: ", *npc.cards, sep='\n ')
    print("NPC's Hand =", npc.value)


def player_busts(player, dealer, chips):
    print("\nPLAYER BUSTS!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    if player.value == 21 and len(player.cards) == 2:
        print("\nPLAYER BLACKJACK!")
        chips.win_bet()
    else:
        print("\nPLAYER WINS!")
        chips.win_bet()
    print(f"Player's Chips: {chips.total}")

def dealer_busts(player, dealer, chips):
    print("\nDEALER BUSTS!")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    if dealer.value == 21 and len(dealer.cards) == 2:
        print("\nDEALER BLACKJACK!")
        chips.lose_bet()
    else:
        print("\nDEALER WINS!")
        chips.lose_bet()
    print(f"Player's Chips: {chips.total}")

def push(player, dealer, npc):
    print("Its a push! Player, Dealer, and NPC tie!")


class GameStats:
    def __init__(self):
        self.games_played = 0
        self.player_wins = 0
        self.dealer_wins = 0
        self.pushes = 0
        self.player_blackjacks = 0
        self.dealer_blackjacks = 0
        self.dealer_surrenders = 0
        self.dealer_folds = 0
        self.npc_wins = 0
        self.npc_blackjacks = 0

    def update_stats(self, player_result, dealer_result=None):
        self.games_played += 1
        if player_result == 'player':
            self.player_wins += 1
        elif player_result == 'player_blackjack':
            self.player_blackjacks += 1
        elif player_result == 'dealer':
            self.dealer_wins += 1
        elif player_result == 'push':
            self.pushes += 1

        if dealer_result == 'dealer_blackjack':
            self.dealer_blackjacks += 1
        elif dealer_result == 'dealer_surrender':
            self.dealer_surrenders += 1
        elif dealer_result == 'dealer_fold':
            self.dealer_folds += 1

        if dealer_result == 'npc':
            self.npc_wins += 1
        elif dealer_result == 'npc_blackjack':
            self.npc_blackjacks += 1

    def show_stats(self):
        print("\nGame Statistics:")
        print(f"Games Played: {self.games_played}")
        print(f"Player Wins: {self.player_wins}")
        print(f"Dealer Wins: {self.dealer_wins}")
        print(f"Pushes: {self.pushes}")
        print(f"Player Blackjacks: {self.player_blackjacks}")
        print(f"Dealer Blackjacks: {self.dealer_blackjacks}")
        print(f"Dealer Surrenders: {self.dealer_surrenders}")
        print(f"Dealer Folds: {self.dealer_folds}")
        print(f"NPC Wins: {self.npc_wins}")
        print(f"NPC Blackjacks: {self.npc_blackjacks}")


def reset_hands(deck, player_hand, dealer_hand, npc_hand):
    player_hand.cards = []
    dealer_hand.cards = []
    npc_hand.cards = []
    player_hand.value = 0
    dealer_hand.value = 0
    npc_hand.value = 0
    player_hand.aces = 0
    dealer_hand.aces = 0
    npc_hand.aces = 0
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    npc_hand.add_card(deck.deal())
    npc_hand.add_card(deck.deal())


def continue_playing():
    while True:
        choice = input("\nWould you like to continue playing? Enter 'y' to continue or 'n' to quit: ")
        if choice.lower() in ['y', 'n']:
            return choice.lower() == 'y'
        else:
            print("Invalid choice. Please enter 'y' or 'n'.")


# GAMEPLAY

player_chips = Chips()
game_stats = GameStats()
npc_player = NPCPlayer("NPC")

while True:
    print(f"\nWelcome to BlackJack, {playername}!\n")

    num_decks = int(input("How many decks would you like to use? "))
    deck_random = Deck(num_decks)

    npc_player = NPCPlayer("NPC")

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()
    npc_hand = Hand()

    player_chips = Chips()
    player_chips.total = display_chips()

    while player_chips.total > 0:
        take_bet(player_chips)
        npc_bet = npc_player.take_bet()
        print(f"{npc_player.name} bets: {npc_bet}")

        reset_hands(deck, player_hand, dealer_hand, npc_hand)

        show_some(player_hand, dealer_hand, npc_hand)

        playing = True
        while playing:
            hit_or_stand(deck, player_hand)
            show_some(player_hand, dealer_hand, npc_hand)

            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                game_stats.update_stats('dealer')
                break

        if player_hand.value <= 21:
            dealer_action = dealer_play(deck, dealer_hand)
            npc_action = npc_play(deck, npc_hand)

            show_all(player_hand, dealer_hand, npc_hand)

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
                push(player_hand, dealer_hand, npc_hand)
                game_stats.update_stats('push')

            if npc_hand.value > 21:
                print("NPC BUSTS!")
                game_stats.update_stats('player', 'npc')
            elif npc_hand.value == 21 and len(npc_hand.cards) == 2:
                print("NPC Blackjack!")
                game_stats.update_stats('player_blackjack', 'npc_blackjack')

        game_stats.show_stats()
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