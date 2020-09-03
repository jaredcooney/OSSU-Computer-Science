"""
Implementation of the game Blackjack
Dealer wins ties

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

WIDTH = 600
HEIGHT = 600

# initialize some useful global variables
in_play = False
outcome = ""
prompt = ""
forfeit_message = ""
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
        self.cards = []

    def __str__(self):
        result = ""
        for i in range(len(self.cards)):
            result += self.cards[i].__str__()
            if i < range(len(self.cards))[-1]:
                result += ", "
        return "hand contains " + result

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        hand_value = 0
        ace_flag = 0
        for c in self.cards:
            hand_value += VALUES[c.get_rank()]
            if c.get_rank() == "A":
                ace_flag = 1
        
        if ace_flag != 1:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
   
    def draw(self, canvas, pos):
        for c in range(len(self.cards)):
            self.cards[c].draw(canvas, [pos[0] + 1.25 * c * CARD_SIZE[0], pos[1] + CARD_SIZE[1]])
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        result = ""
        for i in range(len(self.cards)):
            result += self.cards[i].__str__()
            if i < range(len(self.cards))[-1]:
                result += ", "
        return "Deck contains " + result
    

#define event handlers for buttons
def deal():
    global outcome, prompt, score, in_play, deck, player_hand, dealer_hand, first_game, forfeit_message
    if in_play:
        score -= 1
        forfeit_message = "You have forfeited the previous hand."
    deck = Deck()
    deck.shuffle()    
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    prompt = "Hit or stand?"
    outcome = ""
    in_play = True

def hit():
    global score, prompt, outcome, in_play, forfeit_message
    forfeit_message = ""
    if in_play  and  (player_hand.get_value() <= 21):
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted."
            prompt = "New hand?"
            score -= 1
            in_play = False
       
def stand():
    global score, outcome, prompt, in_play, forfeit_message
    forfeit_message = ""
    if not in_play  and  (player_hand.get_value() > 21):
        outcome = "Nice try. Still busted."
    elif in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "Dealer has busted!"
            score += 1
        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                score -= 1
                outcome = "Dealer wins."
            else:
                score += 1
                outcome = "Player wins!"
        in_play = False
        prompt = "New hand?"

# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", [WIDTH * 0.14, HEIGHT * 0.13], 52, "cyan")
    canvas.draw_text("Dealer", [WIDTH * 0.11, HEIGHT * 0.3], 38, "black")
    canvas.draw_text("Player", [WIDTH * 0.11, HEIGHT * 0.65], 38, "black")
    canvas.draw_text(prompt, [WIDTH * 0.45, HEIGHT * 0.65], 38, "black")
    canvas.draw_text(outcome, [WIDTH * 0.45, HEIGHT * 0.3], 38, "black")
    canvas.draw_text("Score: " + str(score), [WIDTH * 0.7, HEIGHT * 0.125], 38, "black")
    canvas.draw_text(forfeit_message, [WIDTH * 0.1, HEIGHT * 0.95], 32, "maroon")
    
    dealer_hand.draw(canvas, [WIDTH * 0.11, HEIGHT * 0.18])
    player_hand.draw(canvas, [WIDTH * 0.11, HEIGHT * 0.53])
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                         [WIDTH * 0.11 + CARD_SIZE[0] * 0.5, HEIGHT * 0.18 + CARD_SIZE[1] * 1.5], CARD_SIZE)

# create frame
frame = simplegui.create_frame("Blackjack", WIDTH, HEIGHT)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

#start game and frame
deal()
frame.start()
