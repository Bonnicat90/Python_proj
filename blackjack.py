# rules:
# - you can choose numbre of players 
# - you have one automated dealer.
# - players always play first 
# How to win:
#   1) try to get closer to 21 than the dealer without going over 21
#   2) Blackjack: if you get a jack, player automatically wins, and you will get bet 150% of your bet
# You lose when: 
#   1) dealers gets closer to 21 than you 
#   2) you go over 21 
# if you lose you lose all your bet if you win you get same amount of your bet
# card values:
#   1) 2-10 = Face value
#   2) Jack, Queen, King =10 pts
#   3) Ace can be either 1 or 11
# Palying decisions:
#   1) Hitting: getting another card 
#   2) standing: dont want another card
#   3) Splitting:if the two cards have the same value, separate them to make two hands and put a 2nd equal bet out
#   4) Doubling down:  Increase the initial bet by 100%, take only one more card 


import random 
# Global variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
playing = True


#  Create a Card Class
class Card:
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
    def __str__(self):
        return f'{self.rank} of {self.suit}'

# create a class of deck of card for a round
class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))  # build Card objects and add them to the list
    # for checking the results 
    def __str__(self):
        deck_comp = ''  # start with an empty string
        for card in self.deck:
            deck_comp += '\n '+card.__str__() # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

#  Create a Hand Class
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value+=values[card.rank]
        if card.rank=='Ace':
            self.aces+=1
            
    def adjust_for_ace(self):
        # reduce the Ace's value down to 1
        while self.value>21 and self.aces:
            self.value-=10
            self.aces -= 1
        return self.value
    def __str__(self):
        return ', '.join(str(card) for card in self.cards) + f" (Value: {self.value()})"

 
# create player class
class Player:
    def __init__(self, name,chips):
        self.name = name
        self.hand=Hand()
        self.chips = chips

    def __str__(self):
        return f"{self.name}: " + " | ".join(str(hand) for hand in self.hand) + f" (Balance: ${self.total})"

# create a Chip class
class Chips:
    def __init__(self,inibet,bet):
        self.total=inibet
        self.bet=bet
    def win(self):
        self.total+=self.bet
    def lose(self):
        self.total-=self.bet

Chips.win(100,10)

################################################################### 
#############################Functions#############################
################################################################### 
# function of taking bet
def take_bet(chips):
    while True:
        try:
            Chips.bet=int(input("How much would you like to bet? "))   
        except:
            ValueError("Bet has to be a number and between 1 to 100.")
        else:
            if Chips.bet>Chips.total:
                print(f"You only have ${Chips.total}, not enough money.")
            else:
                break

# show cards
def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

# evaluate win and lose:
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose()
def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win()

def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose()
def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win()
    

def push(player,dealer):
    print("Dealer and Player tie! It's a push.")


while True:
    # Print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')

    numplayers=int(input("How many players are playing?"))
    if numplayers<2 or numplayers>7:
            raise ValueError("Number of players must be between 2 and 7")
    
    player_chips=[]
    for i in range(1,numplayers+1):
        player_chips.append(int(input(f"Player {i}, how many chips do you have in hand: ")))

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    players_hands = {}
    for player in players:
        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        players_hands[player] = player_hand

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Players' chips
    players_chips = {player: Chips() for player in players}  # remember the default value is 100

    # Prompt each Player for their bet
    for player in players:
        take_bet(players_chips[player], player)

    # Show cards (but keep one dealer card hidden)
    for player in players:
        show_some(players_hands[player], dealer_hand)

    # Loop through each player's turn
    for player in players:
        player_hand = players_hands[player]

        while playing:  # recall this variable from our hit_or_stand function

            # Prompt for Player to Hit or Stand
            hit_or_stand(deck, player_hand)

            # Show cards (but keep one dealer card hidden)
            show_some(player_hand, dealer_hand)

            # If player's hand exceeds 21, run player_busts() and break out of loop
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, players_chips[player])
                break

    # If all Players haven't busted, play Dealer's hand until Dealer reaches 17
    if all(player_hand.value <= 21 for player_hand in players_hands.values()):
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        for player in players:
            show_all(players_hands[player], dealer_hand)

        # Run different winning scenarios for each player
        for player in players:
            player_hand = players_hands[player]
            player_chips = players_chips[player]

            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)

            else:
                push(player_hand, dealer_hand)

    # Inform each Player of their chips total
    for player in players:
        print(f"\n{player}'s winnings stand at {players_chips[player].total}")

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

    if new_game.lower() != 'y':
        print("Thanks for playing!")
        break
