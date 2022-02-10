"""
Algorithmic Thinking: Project 4
(Rice University)
Topic: Computing and analyzing alignments of DNA and RNA sequences

Student: Jared Cooney
jaredcooney2@gmail.com
"""

######################################################
# Matrix functions

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes a set of characters alphabet and three integer scores diag_score,
    off_diag_score, and dash_score. Returns a dictionary of dictionaries whose
    entries are indexed by pairs of characters in alphabet plus "-". The score
    for an entry indexed by one or more dashes is dash_score; the score for 
    entries whose two indices are equivalent is diag_score; the score for
    all remaining entries is off_diag_score.
    """
    scoring_matrix = {}
    characters = alphabet.union(set(["-"]))
    
    for row_char in characters:
        scoring_matrix[row_char] = {}
        
        for col_char in characters:
            if row_char == "-"  or  col_char == "-":
                scoring_matrix[row_char][col_char] = dash_score
            elif row_char == col_char:
                scoring_matrix[row_char][col_char] = diag_score
            else:
                scoring_matrix[row_char][col_char] = off_diag_score

    return scoring_matrix
            

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes two sequences seq_x and seq_y, whose elements share a common alphabet
    with scoring_matrix. If global_flag is True, this function returns the
    global alignment matrix for the two given sequences using the given scoring 
    matrix. If global_flag is False, it returns the local alignment matrix.

    The alignment matrix is a list of lists, indexed alignment_matrix[row][col]
    """
    alignment_matrix = [[0 for dummy_col in xrange(len(seq_y) + 1)] \
                            for dummy_row in xrange(len(seq_x) + 1)]

    for idx in xrange(1, len(seq_x) + 1):
        alignment_matrix[idx][0] = alignment_matrix[idx - 1][0] + \
                                    scoring_matrix[seq_x[idx - 1]]["-"]
        if not global_flag:
            alignment_matrix[idx][0] = max(0, alignment_matrix[idx][0])

    for idx in xrange(1, len(seq_y) + 1):
        alignment_matrix[0][idx] = alignment_matrix[0][idx - 1] + \
                                    scoring_matrix["-"][seq_y[idx - 1]]
        if not global_flag:
            alignment_matrix[0][idx] = max(0, alignment_matrix[0][idx])


    for x_idx in xrange(1, len(seq_x) + 1):
        for y_idx in xrange(1, len(seq_y) + 1):

            diag_score = alignment_matrix[x_idx - 1][y_idx - 1] + \
                          scoring_matrix[seq_x[x_idx - 1]][seq_y[y_idx - 1]]
            vert_score = alignment_matrix[x_idx - 1][y_idx] + \
                          scoring_matrix[seq_x[x_idx - 1]]["-"]
            horiz_score = alignment_matrix[x_idx][y_idx - 1] + \
                          scoring_matrix["-"][seq_y[y_idx - 1]]

            optimal_score = max(diag_score, vert_score, horiz_score)
            alignment_matrix[x_idx][y_idx] = optimal_score

            if not global_flag:
                alignment_matrix[x_idx][y_idx] = \
                                        max(0, alignment_matrix[x_idx][y_idx])

            
    return alignment_matrix

######################################################
# Helper function

def highest_matrix_entry(matrix):
    """
    Takes a matrix (a list of lists) with numeric entries; returns
    the entry with the highest value and its indices as a tuple 
    with the form (highest_value, row, col)
    """
    row = -1
    col = -1
    highest_value = -float('inf')
    for row_idx in xrange(len(matrix)):
        for col_idx in xrange(len(matrix[row_idx])):
            if matrix[row_idx][col_idx] > highest_value:
                highest_value = matrix[row_idx][col_idx]
                row = row_idx
                col = col_idx
                
    return (highest_value, row, col)

######################################################
# Alignment functions

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes two sequences seq_x and seq_y, whose elements share a common alphabet
    with the given scoring matrix. Returns the optimal global alignment of the
    two sequences using the scoring matrix and the given alignment matrix.

    Output is a tuple of the form (score, align_x, align_y), where
    score is the score of the global alignment align_x and align_y
    according to the scoring matrix.
    """

    # initialize traceback indices and (empty) output sequences
    x_idx = len(seq_x)
    y_idx = len(seq_y)
    align_x = ""
    align_y = ""

    # Trace back through alignment matrix to build optimal global alignment
    # sequences. Start at final entry and go all the way back to entry [0, 0]
    while x_idx > 0  and  y_idx > 0:
        current_entry = alignment_matrix[x_idx][y_idx]

        # if the previous entry is above and to the left of the current entry
        if current_entry == alignment_matrix[x_idx - 1][y_idx - 1] + \
                             scoring_matrix[seq_x[x_idx - 1]][seq_y[y_idx - 1]]:
            align_x = seq_x[x_idx - 1] + align_x
            align_y = seq_y[y_idx - 1] + align_y
            x_idx -= 1
            y_idx -= 1

        # if the previous entry is directly above the current entry
        elif current_entry == alignment_matrix[x_idx - 1][y_idx] + \
                               scoring_matrix[seq_x[x_idx - 1]]["-"]:
            align_x = seq_x[x_idx - 1] + align_x
            align_y = "-" + align_y
            x_idx -= 1

        # if the previous entry is directly to the left of the current entry
        elif current_entry == alignment_matrix[x_idx][y_idx - 1] + \
                               scoring_matrix["-"][seq_y[y_idx - 1]]:
            align_x = "-" + align_x
            align_y = seq_y[y_idx - 1] + align_y
            y_idx -= 1
        
        else:
            print "Error: compute_global_alignment could not find \
                   a valid path during traceback."
            print "Current index: [" + str(x_idx) + ", " + str(y_idx) + "]"
            print "Current entry:", current_entry
            return


    while x_idx > 0:
        align_x = seq_x[x_idx - 1] + align_x
        align_y = "-" + align_y
        x_idx -= 1

    while y_idx > 0:
        align_x = "-" + align_x
        align_y = seq_y[y_idx - 1] + align_y
        y_idx -= 1


    return (alignment_matrix[-1][-1], align_x, align_y)



def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes two sequences seq_x and seq_y, whose elements share a common alphabet
    with the given scoring matrix. Returns the optimal local alignment of
    the two sequences using the scoring matrix and the given alignment matrix.

    Output is a tuple of the form (score, align_x, align_y), where
    score is the score of the optimal local alignment align_x and align_y
    according to the scoring matrix.
    """
    
    # find the indices of the highest-scored entry in the alignment matrix
    highest_score, x_idx, y_idx = highest_matrix_entry(alignment_matrix)

    # initialize output sequences to empty strings
    align_x = ""
    align_y = ""

    # Trace back through alignment matrix to build optimal local alignment
    # sequences. Start at highest-scored entry; stop when we reach
    # an entry with a score of zero
    finished_flag = False
    while x_idx > 0  and  y_idx > 0  and  not finished_flag:
        current_entry = alignment_matrix[x_idx][y_idx]
        
        # if the previous entry is above and to the left of the current entry
        if current_entry == alignment_matrix[x_idx - 1][y_idx - 1] + \
                             scoring_matrix[seq_x[x_idx - 1]][seq_y[y_idx - 1]]:
            previous_entry = alignment_matrix[x_idx - 1][y_idx - 1]
            align_x = seq_x[x_idx - 1] + align_x
            align_y = seq_y[y_idx - 1] + align_y
            x_idx -= 1
            y_idx -= 1

        # if the previous entry is directly above the current entry
        elif current_entry == alignment_matrix[x_idx - 1][y_idx] + \
                               scoring_matrix[seq_x[x_idx - 1]]["-"]:
            previous_entry = alignment_matrix[x_idx - 1][y_idx]
            align_x = seq_x[x_idx - 1] + align_x
            align_y = "-" + align_y
            x_idx -= 1

        # if the previous entry is directly to the left of the current entry
        else:
            previous_entry = alignment_matrix[x_idx][y_idx - 1]
            align_x = "-" + align_x
            align_y = seq_y[y_idx - 1] + align_y
            y_idx -= 1

        if previous_entry == 0:
            finished_flag = True


    while x_idx > 0  and  not finished_flag:
        align_x = seq_x[x_idx - 1] + align_x
        align_y = "-" + align_y
        x_idx -= 1
        if alignment_matrix[x_idx - 1][0] == 0:
            finished_flag = True
        
    while y_idx > 0  and  not finished_flag:
        align_x = "-" + align_x
        align_y = seq_y[y_idx - 1] + align_y
        y_idx -= 1
        if alignment_matrix[0][y_idx - 1] == 0:
            finished_flag = True

              
    return (highest_score, align_x, align_y)

###############################################################################
###############################################################################
# Application 3

import urllib2
import numpy as np
import random

######################################################################
# Provided code for loading the analysis data

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename 

    Returns a dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict

def read_protein(filename):
    """
    Read a protein sequence from the file named filename
    
    Returns a string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq

def read_words(filename):
    """
    Load word list from the file named filename; returns a list of strings
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list

######################################################################
# Question 1: Local alignment of human and fruitfly eyeless protein sequences

human_eyeless_protein = read_protein(HUMAN_EYELESS_URL)
fruitfly_eyeless_protein = read_protein(FRUITFLY_EYELESS_URL)

pam50_score_matrix = read_scoring_matrix(PAM50_URL)
eyeless_alignment_matrix = compute_alignment_matrix(human_eyeless_protein, \
                            fruitfly_eyeless_protein, pam50_score_matrix, \
                            False)

eyeless_alignment = compute_local_alignment(human_eyeless_protein,
                     fruitfly_eyeless_protein, pam50_score_matrix,
                     eyeless_alignment_matrix)

print "The optimal local alignment of the human and fruitfly eyeless protein " \
        + "sequences according to the PAM50 scoring matrix has score " \
        + str(eyeless_alignment[0]) + " and length " \
        + str(len(eyeless_alignment[1]))+ "."

print "The alignment is as follows.\n"

print "Aligned human sequence below:\n", eyeless_alignment[1]
print "\n", eyeless_alignment[2], "\nAligned fruitfly sequence above ^"


# The score of the alignment of the human and fruitfly eyeless protein
#  sequences is 875.

# The alignment is as follows, with the aligned human sequence presented first:
# HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEK-QQ
# HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ

##########################################################
# Question 2: Comparing local alignment sequences from Question 1 to
#             the Consensus PAX Domain

consensus_pax_domain = read_protein(CONSENSUS_PAX_URL)

# remove any dashes from the local alignment sequences generated in Question 1
human_pax_sequence = "HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ"
fly_pax_sequence = "HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ"

# compute comparison alignment matrices and alignments
human_consensus_align_matrix = compute_alignment_matrix(human_pax_sequence,
                               consensus_pax_domain, pam50_score_matrix, True)
fly_consensus_align_matrix = compute_alignment_matrix(fly_pax_sequence,
                             consensus_pax_domain, pam50_score_matrix, True)

human_consensus_alignment = compute_global_alignment(human_pax_sequence,
                            consensus_pax_domain, pam50_score_matrix,
                            human_consensus_align_matrix)
fly_consensus_alignment = compute_global_alignment(fly_pax_sequence,
                          consensus_pax_domain, pam50_score_matrix,
                          fly_consensus_align_matrix)


# compute percentages of amino acids that match between the aligned sequences
human_consensus_align_length = len(human_consensus_alignment[1])
fly_consensus_align_length = len(fly_consensus_alignment[1])

human_consensus_align_matches = 0
fly_consensus_align_matches = 0

for idx in xrange(human_consensus_align_length):
    if human_consensus_alignment[1][idx] == human_consensus_alignment[2][idx]:
        human_consensus_align_matches += 1

for idx in xrange(fly_consensus_align_length):
    if fly_consensus_alignment[1][idx] == fly_consensus_alignment[2][idx]:
        fly_consensus_align_matches += 1
        
human_consensus_match_percent = 100 * float(human_consensus_align_matches)  \
                                   / human_consensus_align_length
fly_consensus_match_percent = 100 * float(fly_consensus_align_matches)  \
                                   / fly_consensus_align_length


print "\n\nWhen the previously-computed locally aligned human sequence is " \
      + "globally aligned with the consensus PAX domain, the result is as " \
      + "follows, with the aligned human sequence above the consensus sequence:"
print human_consensus_alignment[1]
print human_consensus_alignment[2]
print str(human_consensus_match_percent) + "% of these paired elements match."

print "\nWhen the previously-computed locally aligned fruitfly sequence " \
      + "is globally aligned with the consensus PAX domain, the result " \
      + "is as follows, with the aligned fruitfly sequence above " \
      + "the consensus sequence:"
print fly_consensus_alignment[1]
print fly_consensus_alignment[2]
print str(fly_consensus_match_percent) + "% of these paired elements match."


# Global alignment of local human sequence vs consensus PAX domain:
#  -HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ
#  GHGGVNQLGGVFVNGRPLPDVVRQRIVELAHQGVRPCDISRQLRVSHGCVSKILGRYYETGSIKPGVIGGSKPKVATPKVVEKIAEYKRQNPTMFAWEIRDRLLAERVCDNDTVPSVSSINRIIR--------
# 72.93% of the paired elements match in this alignment.

# Global alignment of the local fruitfly sequence vs consensus PAX domain:
#  -HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ
#  GHGGVNQLGGVFVNGRPLPDVVRQRIVELAHQGVRPCDISRQLRVSHGCVSKILGRYYETGSIKPGVIGGSKPKVATPKVVEKIAEYKRQNPTMFAWEIRDRLLAERVCDNDTVPSVSSINRIIR---------
# 70.15% of the paired elements match in this alignment.

########################################################
# Question 3: Examining the liklihood that the level of similarity exhibited
#             in questions 1 and 2 is due to chance

# Assuming an equal probability of any amino acid appearing at a given location
#  in a sequence, an application of the cumulative distribution function
#  demonstrates that it is astronomically unlikely that the similarity of any
#  of the above sequences arose by chance.

# For a ballpark example, given an alignment with length 100 of two sequences
#  of randomly-selected amino acids, the probability that at least 70%
#  of the elements match is approximately 3.769 x 10^-71, which is so small
#  that many calculators will simply return zero.

########################################################
# Question 4: Generating a null distribution for scores of local alignments
#             of the human and fruitfly eyeless protein sequences


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Takes two sequences, a scoring matrix, and a number of trials;
    In each trial, seq_x is locally aligned with a random permutation of
    seq_y, and the score of the resulting alignment is recorded.
    Returns the unnormalized distribution of these scores as a dictionary.
    
    """
    scoring_distribution = {}
    for dummy_trial in xrange(num_trials):
        rand_y = [seq_y[idx] for idx in xrange(len(seq_y))]
        random.shuffle(rand_y)
        matrix = compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = highest_matrix_entry(matrix)[0]
        if score in scoring_distribution:
            scoring_distribution[score] += 1
        else:
            scoring_distribution[score] = 1

    return scoring_distribution


##NUM_TRIALS = 1000
##null_dist = generate_null_distribution(human_eyeless_protein, \
##                fruitfly_eyeless_protein, pam50_score_matrix, NUM_TRIALS)
##
##normalized_null_dist = {score : float(frequency) / NUM_TRIALS \
##                            for (score, frequency) in null_dist.items()}


# I used numpy to export plot data to a CSV file
##np.savetxt('NormNullData.csv', \
##           [item for item in normalized_null_dist.items()], \
##           delimiter=',', fmt='%s')


# View the resulting null distribution plot here:
# https://www.dropbox.com/s/2niucjeu4q7xsno/NullDistPlot.png?dl=0

########################################################
# Question 5: A statistical analysis of the null distribution from Question 4

##mean_null_score = 0
##null_standard_dev = 0
##
##for item in null_dist.items():
##    mean_null_score += item[0] * item[1]
##mean_null_score /= float(NUM_TRIALS)
##
##for item in null_dist.items():
##    null_standard_dev += ((item[0] - mean_null_score) ** 2) * item[1]
##null_standard_dev /= float(NUM_TRIALS)
##null_standard_dev **= 0.5
##
##human_fly_local_zscore = (eyeless_alignment[0] - mean_null_score)  \
##                          / null_standard_dev

##print "\n\nMean score for this set of null hypothesis trials:", mean_null_score
##print "Standard deviation:", null_standard_dev
##
##print "Based on these values, the z-score for the local alignment of the " \
##      + "human and fruitfly eyeless proteins is " + str(human_fly_local_zscore)


# The mean score of the (first) null distribution generated above was 52.011
# The standard deviation was 7.0874

# Based on these values, the z-score for the local alignment of the human and
#  fruitfly eyeless proteins (from question 1) is around 116

########################################################
# Question 6: Further analyzing the liklihood that the level of 
#             similarity exhibited in question 1 is due to chance

# The score resulting from the local alignment of the HumanEyelessProtein
#  and the FruitflyEyelessProtein is not due to chance.

# The probability per entry of winning the jackpot in a large lottery can
#  be as low as approximately 1 in 300,000,000. The probability that the
#  similarity between the aforementioned proteins is due to chance is many
#  orders of magnitude lower.
#  The null distribution generated in Question 6 resembles a normal
#  distribution, and, as mentioned in the prompt, it is extremely 
#  rare (<0.27%) that a realization of a normally distributed random
#  variable falls more than three standard deviations from the mean.
#  In this case, the score for the local alignment is about 116 standard
#  deviations away from the mean, so it is quite safe to say that it does
#  not belong to the null distribution.

#  Also see Question 3 for a ballpark probability estimate.

########################################################
# Question 7: Considering string similarity and a scoring matrix that
#             can be used to compute edit distance

# For the given edit distance formula...

# diag_score is 2
# off_diag_score is 1
# dash_score is 0

# I found these values by setting up equations of the form
#  >> |x| + |y| - score(x, y) = edit_distance
#  for three pairs of simple words that were easy to globally align
#  "manually", then rewriting score(x, y) in terms of the appropriate 
#  scoring matrix values and solving for those values.

########################################################
# Question 8: Implementing a simple spell-checker function

print "\n"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"
word_list = read_words(WORD_LIST_URL)

spelling_alphabet = {char for char in "abcdefghijklmnopqrstuvwxyz"}
edit_dist_score_matrix = build_scoring_matrix(spelling_alphabet, 2, 1, 0)


def find_edit_distance(word1, word2, scoring_matrix):
    """
    Uses the given scoring matrix to calculate and return the edit distance
    between the given strings word1 and word2 based on the formula
    >> edit_distance = |x| + |y| - score(x, y)
    """
    alignment_matrix = compute_alignment_matrix(word1, word2, \
                                                scoring_matrix, True)
    
    score = compute_global_alignment(word1, word2, scoring_matrix, \
                                     alignment_matrix)[0]

    return len(word1) + len(word2) - score


def check_spelling(checked_word, dist, word_list):
    """
    Returns the set of all words in word_list that are at most 
    edit distance dist away from the string checked_word
    """
    similar_words = set([])
    
    for word in word_list:
        edit_distance = find_edit_distance(checked_word, word, \
                                           edit_dist_score_matrix)
        if edit_distance <= dist:
            similar_words.add(word)

    return similar_words


print "\nWords within an edit distance of 1 from the string 'humble':"
print check_spelling("humble", 1, word_list)
print "\nWords within an edit distance of 2 from the string 'firefly':"
print check_spelling("firefly", 2, word_list)

# Words within an edit distance of 1 from the string "humble":
#  'bumble', 'humbled', 'tumble', 'humble', 'rumble', 'humbler',
#  'humbles', 'fumble', 'humbly', 'jumble', 'mumble'

# Words within an edit distance of 2 from the string "firefly":
#  'firefly', 'tiredly', 'freely', 'fireclay', 'direly', 'finely',
#  'firstly', 'liefly', 'fixedly', 'refly', 'firmly'

########################################################
# Question 9: Considering a more efficient spell-checker algorithm

# The algorithm in Question 8 is relatively inefficient because it iterates
#  through the entire word list.

# A more efficient algorithm for small values of the given edit distance dist
#  would instead first convert the word list to a set. Then it would
#  consider all possible strings that can be created by applying dist or
#  fewer edit operations (substitutions, insertions, and deletions) to the
#  input word, and checking these strings against the word
#  set to determine whether they are valid words.

##############################################################################
print "\nFinished running =)"


