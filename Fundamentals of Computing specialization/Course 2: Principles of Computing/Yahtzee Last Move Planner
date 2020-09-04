"""
Simplified Last Move Planner for Yahtzee
Simplifications: Only allow discard and roll, only score against upper level of score sheet

Student: Jared Cooney
jaredcooney2@gmail.com
"""

# Used to increase the runtime limit, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of
    all sequences of outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according
    to the upper section of the Yahtzee score card.
    
    hand: full yahtzee hand as a tuple
    
    Returns an integer score 
    """
    score_per_num = [hand.count(num) * num for num in range(1, max(hand) + 1)]
    return max(score_per_num)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold (as a tuple)
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    expected = 0
    partial_seqs = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    seqs = [list(seq) for seq in partial_seqs]
    for seq in seqs:
        seq.extend(held_dice)
        expected += score(seq) / float(len(seqs))
    return expected


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand as a tuple
    
    Returns a set of tuples, where each tuple is dice to hold
    """
    holds = set([()])
    for dummy_idx in range(len(hand)):
        temp_set = set()
        for hold in holds:
            temp_hand = list(hand)
            for num in hold:
                temp_hand.remove(num)            
            for num in temp_hand:
                new_hold = list(hold)
                new_hold.append(num)
                new_hold.sort()
                temp_set.add(tuple(new_hold))
        holds.update(temp_set)
    return holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand as a tuple
    num_die_sides: number of sides on each die
    
    Returns a tuple where the first element is the expected score
    and the second element is a tuple of the dice to hold
    """
    max_expected = 0
    best_hold = None
    holds = gen_all_holds(hand)
    for hold in holds:
        expected = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if expected > max_expected:
            max_expected = expected
            best_hold = hold
    return (max_expected, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    
    # modify this for different hands
    hand = (1, 1, 1, 5, 6)
    
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, \
    "with expected score", hand_score
    
    
run_example()

# Testing######################################################
#import user47_NZUCUtAm0H_18 as poc_yahtzee_testsuite
#poc_yahtzee_testsuite.run_gen_all_holds_suite(gen_all_holds)
#poc_yahtzee_testsuite.run_score_suite(score)
#poc_yahtzee_testsuite.run_expected_value_suite(expected_value)
#poc_yahtzee_testsuite.run_strategy_suite(strategy)
