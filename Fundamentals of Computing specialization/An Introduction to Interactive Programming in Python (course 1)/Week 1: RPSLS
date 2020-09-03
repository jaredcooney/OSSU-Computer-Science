"""
Rock-paper-scissors-lizard-Spock

Simple implentation of an expanded version of
the classic game rock-paper-scissors. Type
your choice in the input field.

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random
import simplegui

#helper function
def name_to_number(name):
    """Takes the RSPLS player's choice and returns the corresponding number from 0 to 4"""

    if   name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print 'ERROR: Invalid input "' + str(name) + '".' 
        print 'The options are "rock"',
        print '"paper", "scissors", "lizard", and "Spock" (case-sensitive).'

#helper function
def number_to_name(number):
    """Takes a number from 0 to 4 and returns the corresponding RSPLS choice."""
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print 'Error: Function number_to_name received an invalid input, "' + str(number) + '".'
        return 9
    
#input event handler function
def rpsls(player_choice): 
    # print a blank line to separate consecutive games
    print

    # print out the message for the player's choice
    print "Player chooses " + str(player_choice) + "."

    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    if player_number != None:
    
        # compute random guess for comp_number using random.randrange()
        comp_number = random.randrange(0, 5)
    
        # convert comp_number to comp_choice using the function number_to_name()
        comp_choice = number_to_name(comp_number)
    
        # print out the message for computer's choice
        print "Computer chooses " + str(comp_choice) + "."

        # compute difference of comp_number and player_number modulo five
        diff = (player_number - comp_number) % 5
    
        # use if/elif/else to determine winner, print winner message
        if diff == 1 or diff == 2:
            print "Player wins!"
        elif diff == 3 or diff == 4:
            print "Computer wins!"
        elif diff == 0:
            print "It's a tie!"
        else:
            print "Error. Variable diff received an input that is not a number from 0 to 4."

    else:
        print "Please try again with a valid choice."
    
    
frame = simplegui.create_frame("RPSLS Game", 200, 200)

frame.add_input("Enter your RSPLS choice here:", rpsls, 50)
    
frame.start()
