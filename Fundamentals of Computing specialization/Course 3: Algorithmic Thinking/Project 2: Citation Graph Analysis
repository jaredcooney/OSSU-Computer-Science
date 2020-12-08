"""
Algorithmic Thinking: Project 1

Student: Jared Cooney
jaredcooney2@gmail.com

View and run this project with an in-browser python interpreter at
http://www.codeskulptor.org/#user47_wKn3tnO37r_6.py
"""

# Constant graphs for testing

EX_GRAPH0 = {
            0: set([1,2]),
            1: set([]),
            2: set([])        
            }

EX_GRAPH1 = {
            0: set([1, 4, 5]),
            1: set([2, 6]),
            2: set([3]),
            3: set([0]),
            4: set([1]),
            5: set([2]),
            6: set([])
            }

EX_GRAPH2 = {
            0: set([1, 4, 5]),
            1: set([2, 6]),
            2: set([3, 7]),
            3: set([7]),
            4: set([1]),
            5: set([2]),
            6: set([]),
            7: set([3]),
            8: set([1, 2]),
            9: set([0, 3, 4, 5, 6, 7])
            }

def make_complete_graph(num_nodes):
    """
    Returns a dictionary representation of the complete
    graph with the given number of nodes
    """
    complete_graph = {}
    for idx in xrange(num_nodes):
        complete_graph[idx] = set((num for num in xrange(num_nodes) \
                                   if num != idx))
    return complete_graph


# Functions to compute degree distribution info ###############################


def compute_in_degrees(digraph):
    """
    Returns a dictionary representing the in-degree
    of each node in the given digraph
    """
    in_degrees = {}
    for node in digraph:
        in_degrees[node] = 0        
        
    for tail_node in digraph:
        for head_node in digraph[tail_node]:
            in_degrees[head_node] += 1
            
    return in_degrees
        

def in_degree_distribution(digraph):
    """
    Returns a dictionary representing the unnormalized in-degree distribution
    for the given digraph; keys are the in-degrees present in the digraph
    """
    in_degrees = compute_in_degrees(digraph)
    distribution = {}
    
    # initialize all degrees to zero occurrences
    for degree in xrange(len(digraph)):
        distribution[degree] = 0
        
    # increment each degree by 1 for each occurrence
    for degree in in_degrees.values():
        distribution[degree] += 1
       
    # remove the degrees that still have zero occurrences
    remove_list = [degree for degree in distribution
                   if distribution[degree] == 0]
    
    for degree in remove_list:
        del distribution[degree]       
            
    return distribution

###############################################################################
# Application #1

# Code for loading physics citation graph ##################
import urllib2
CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)

############################################################
# QUESTION 1: Regarding the citation graph in-degree distribution plot

import math
import numpy as np

citation_dist = in_degree_distribution(citation_graph)
del citation_dist[0]

normalized_citation_dist = {node : float(in_degree) / len(citation_graph) \
                            for (node, in_degree) in citation_dist.items()}

# we could apply the log/log scale manually:
##loglog_normalized_dist = [(math.log(item[0]), math.log(item[1])) \
##                          for item in normalized_citation_dist.items()]


# I used the following code to export the plot data to a CSV file
##np.savetxt('CitationData.csv', \
##           [item for item in normalized_citation_dist.items()], \
##           delimiter=',', fmt='%s')


#   The resulting graph demonstrates that most papers were cited few times,
#    while relatively few papers were cited many times.
#    The log/log plot is approximately linear with negative slope,
#    suggesting that the in-degree distribution is best represented
#    by a power function with a small negative exponent.

############################################################
# QUESTION 2: Regarding the Erdos-Renyi algorithm (which creates
# a graph wherein each node has a directed edge to each of 
# the n - 1 other nodes with probability p)

    # a. Yes, the expected value for the in-degree of each node is the same.
    # b. The in-degree distribution for this graph is a binomial distribution.
    #     It looks like a bell curve with its peak at the expected
    #     in-degree value.
    # c. No, the shape of the ER graph's in-degree distribution plot does not
    #     look like the plot from the citation graph. The ER distribution plot
    #     descends approximately linearly, as higher in-degrees are less
    #     common. Meanwhile, the citation distribution plot is bell-shaped,
    #     with in-degree values near the expected value having higher frequency
    #     than those further away.

############################################################
# QUESTION 3: Choosing n and m to use in constructing a DPA graph

avg_outdeg = 0
for node in citation_graph:
    avg_outdeg += len(citation_graph[node])
avg_outdeg /= float(len(citation_graph))

##print avg_outdeg
# The average out-degree for nodes in the citation graph is ~12.7

    # n <- 27,770 nodes
    # m <- 13 edges added per iteration (at most)

############################################################
# QUESTION 4: Implement the DPA algorithm, compute a graph using the 
# inputs from question 3, and plot the in-degree distribution

import random

def create_DPA(num_nodes, edges_per_iter):
    """
    Generates a graph using DPA algorithm; num_nodes is a positive integer,
    edges_per_iter is a positive integer less than or equal to num_nodes
    """
    if edges_per_iter > num_nodes  or  num_nodes < 1 or edges_per_iter < 1:
        print "Invalid input passed to function create_DPA"
        return
    
    graph = make_complete_graph(edges_per_iter)
    node_pool = []
    for node in graph:
        node_pool.extend([node] * (edges_per_iter))
    
    for num in xrange(edges_per_iter, num_nodes):
        new_edge_heads = set()
        for dummy_idx in xrange(edges_per_iter):
            new_edge_heads.add(random.choice(node_pool))
        graph[num] = new_edge_heads
        node_pool.extend(new_edge_heads)
        node_pool.append(num)
        
    return graph

DPA_graph = create_DPA(27770, 13)
DPA_dist = in_degree_distribution(DPA_graph)
del DPA_dist[0]

normalized_DPA_dist = {node : float(in_degree) / len(DPA_graph) \
                            for (node, in_degree) in DPA_dist.items()}

# I again used the following code to export the plot data to a CSV file
##np.savetxt('DPA_data.csv', \
##           [item for item in normalized_DPA_dist.items()], \
##           delimiter=',', fmt='%s')

############################################################
# QUESTION 5:

# The log/log plot of the DPA graph in-degree distribution is very similar
#  to that of the citation graph. As expected, relatively few nodes have
#  high in-degrees because at each iteration of the algorithm, the nodes with
#  the highest current in-degrees have the highest likelihood of being chosen
#  as heads for newly generated edges.

# This is a great demonstration of the "rich get richer" phenomenon, as the
#  "rich" nodes (those with relatively high in-degrees) are the most likely to
#  have their in-degrees further increased at each iteration, creating a
#  snowball effect and leaving the rest of the "poor" nodes with a much lower
#  probability of being selected for a new edge.
#  In this implementation of the algorithm, the first m nodes generated are
#  initialized with in-degree m - 1, while all subsequently-added nodes begin
#  with in-degree 0, so the first m nodes are especially likely to "get richer".

# This structure in the physics paper citation graph can be understood by
#  considering two concepts. Firstly, papers are published sequentially, not
#  all at once, just as the DPA algorithm adds new nodes and edges iteratively.
#  Secondly, the most popular and renowned papers in the physics community are
#  the ones that will be cited most frequently, both because they will be known
#  to the most researchers, and (though not part of the algorithm) because
#  their contents are presumably of relatively high quality and utility. The
#  additional citations gained due to this popularity will further augment the
#  effect, and these papers will become disproportionately influential.

################################################################################
