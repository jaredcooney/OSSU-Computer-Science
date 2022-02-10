"""
Word Wrangler game

Enter a word in the top input field, then use the bottom input field
to try to guess all of the English words you can make using the letters
from that word. If you get stuck, click a hidden word to reveal it.

The functions set, sort, and sorted are not allowed in this code.
Furthermore, functions in this project should not mutate their inputs.

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
#import user47_Gd7pRcf8Pr_17 as test_suite

codeskulptor.set_timeout(30)

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.
    
    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    This function can be iterative.
    """
    result = list(list1)
    remove_list = []
    for idx in xrange(len(result) - 1):
        if result[idx] == result[idx + 1]:
            remove_list.append(result[idx])
            
    for item in remove_list:
        result.remove(item)
    return result


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.
    
    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    This function can be iterative.
    """
# Got this more efficient version from someone on the forum
    intersection = [] 
    lst1, lst2 = list(list1), list(list2)
                                   
    idx1, idx2 = 0, 0
    while idx1 < len(lst1) and idx2 < len(lst2):
        if lst1[idx1] == lst2[idx2]:
            intersection.append(lst1[idx1])
            idx1 += 1
            idx2 += 1
        elif lst1[idx1] < lst2[idx2]:            
            idx1 += 1
        else:
            idx2 += 1        
    
    return intersection

# First version: passes OwlTest but is relatively inefficient
#    intersection = []
#    for item in list1:
#        current = item
#        min_dupes = min(list1.count(item), list2.count(item))
#        if current not in intersection:
#            intersection.extend([item] * min_dupes)
#    return intersection


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two given ascending-sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.
    This function can be iterative.
    """
    lst1, lst2 = list(list1), list(list2)
    
    result = []
    for item in lst1:
        added = False
        while not added and len(lst2) > 0:
            if lst2[0] < item:
                result.append(lst2.pop(0))
            else:
                result.append(item)
                added = True      
        if not added:
            result.append(item)
    result.extend(lst2)
    
    return result

#   This also works and is arguably more straightforward
#    but contains a bit of repeated code:
#
#    lst1, lst2 = list(list1), list(list2)
#
#    result = []
#    for item in lst1:
#        added = False
#        while not added:
#            if len(lst2) > 0:
#                if lst2[0] < item:
#                    result.append(lst2.pop(0))
#                else:
#                    result.append(item)
#                    added = True  
#            else:
#                result.append(item)
#                added = True   
#
#    result.extend(lst2)
#
#    return result
                                   
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.
    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    
    mid = len(list1) / 2
    left = merge_sort(list1[:mid])
    right = merge_sort(list1[mid:])

    return merge(left, right)


# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.
    This function should be recursive.
    """
    if len(word) == 0:
        return [word]
    
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    
    new_strings = []
    for string in rest_strings:
        for idx in range(len(string) + 1):
            new_strings.append(string[:idx] + first + string[idx:])
    
    return rest_strings + new_strings


# Function to load words from a file
def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    dictionary = urllib2.urlopen(url)
    word_list = [word[:-1] for word in dictionary.readlines()]
    return word_list


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

    
run()


#TESTING
#test_suite.run_suite_remove_duplicates(remove_duplicates)
#test_suite.run_suite_intersect(intersect)
#test_suite.run_suite_merge(merge)
#test_suite.run_suite_merge_sort(merge_sort)
#test_suite.run_suite_gen_all_strings(gen_all_strings)
    
