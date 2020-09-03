# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import math
import random

max = 100
count = 7

# helper function to start and restart the game12
def new_game():
    global secret_number, count
    secret_number = random.randrange(0, max)
    if max == 100:
        count = 7
    else:
        count = 10
    print "New game! Range is 0 to " + str(max)
    print str(count) + " guesses remaining."
    print
    
# define event handlers for control panel
def range100():
    """button that changes the range to [0,100) and starts a new game""" 
    global max, count
    max = 100
    
    print
    new_game()
    
    
def range1000():
    """button that changes the range to [0,1000) and starts a new game"""     
    global max, count
    max = 1000
    
    print
    new_game()
    
    
def input_guess(guess):
    """Handler for input event"""
    global count
    print "Guess was " + guess
    guess_int = int(guess)
    count -= 1
    
    if guess_int == secret_number:
        print "Correct!"
        print
        new_game()
    elif count == 0:
        print "Out of guesses! Number was " + str(secret_number) + ".",
        print "Better luck next time."
        print
        new_game()
    elif guess_int < secret_number:
        print "Higher!"
        print str(count) + " guesses remaining."
        print
    elif guess_int > secret_number:
        print "Lower!"
        print str(count) + " guesses remaining."
        print
    else:
        print "Error: Function input_guess thinks guess_int is"
        print "not higher, lower, nor equal to secret_number???"
    
# create frame
frame = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100)
frame.add_button("Range is [0,1000)", range1000)
frame.add_input("Enter a guess:", input_guess, 50)

frame.start()

# call new_game 
new_game()

