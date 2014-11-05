# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        ans = "Hand contains "
        for card in self.hand:
            ans += (str(card) + " ")
        return ans

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for card in self.hand:
            rank = card.get_rank()
            value += VALUES[rank]
        for card in self.hand:
            if card.get_rank() == 'A' and (value + 10) <= 21:
                value += 10  
        return value
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        n = len(self.hand)
        for i in range(n):
            new_pos = [pos[0] + i * CARD_SIZE[0], pos[1]] 
            self.hand[i].draw(canvas, new_pos)
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
        
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        card = self.deck.pop()
        return card
    
    def __str__(self):
        # return a string representing the deck
        ans = "Deck contains "
        for card in self.deck:
            ans += (str(card) + " ")
        return ans


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score
    
    outcome = "Hit or stand?" 
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    print str(deck)
    print "player  card" + str(player)
    print "dealer  card" + str(dealer)
    in_play = True

def hit():
    global outcome, in_play, deck, player, dealer, score
    # if the hand is in play, hit the player
    if in_play and player.get_value() <= 21:
        player.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    if in_play and player.get_value() > 21:
        print "You have busted"
        in_play = False
        score -= 1
        outcome = "New deal?"
        
def stand():
    global outcome, in_play, deck, player, dealer, score
    outcome = "New deal?"
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())  
        
        # assign a message to outcome, update in_play and score
        print "player score",player.get_value()
        print "dealer score",dealer.get_value()
        if dealer.get_value() > 21:
            print "dealer busts"
            score += 1
        elif player.get_value() <= dealer.get_value():
            score -= 1
            print "player lose"
        else:
            score += 1
            print "player win"
        in_play = False
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global score, outcome
    canvas.draw_text("Blackjack", [50,100], 40, "Black")
    canvas.draw_text("Score "+ str(score), [300,100], 30, "Black")
    canvas.draw_text("Dealer", [50,200], 30, "Black")
    canvas.draw_text("Player", [50,400], 30, "Black")
    canvas.draw_text(outcome, [300,400], 30, "Black")
    player.draw(canvas, [50, 450])
    dealer.draw(canvas, [50, 250])        
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 250 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
