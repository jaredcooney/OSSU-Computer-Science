"""
Algorithmic Thinking: Project 2
(Rice University)

Student: Jared Cooney
jaredcooney2@gmail.com

View the plot images generated in this project here:
https://www.dropbox.com/sh/s2dqo92nagqyebe/AAAXeOeAXVHPOOJ2LvN5eLTLa?dl=0
"""

from collections import deque
import urllib2
import random
import time
import math
import numpy as np

############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    
##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

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

###############################################################################
# Project 2: breadth-first search, connected components, and graph resilience

def bfs_visited(ugraph, start_node):
    """
    Takes an undirected graph and an initial node and returns the
    set of all nodes that have a path to the initial node
    """
    boundary = deque()
    visited = set([start_node])
    boundary.append(start_node)
    
    while len(boundary) != 0:
        current_node = boundary.popleft()
        for neighbor in ugraph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                boundary.append(neighbor)
                
    return visited


def cc_visited(ugraph):
    """
    Takes an undirected graph and returns a list containing
    each set of connected components in the graph.
    """
    remaining_nodes = set([node for node in ugraph.keys()])
    connected_components = []

    while len(remaining_nodes) != 0:
        current_node = remaining_nodes.pop()
        current_component_nodes = bfs_visited(ugraph, current_node)
        connected_components.append(current_component_nodes)
        remaining_nodes.difference_update(current_component_nodes)
        
    return connected_components


def largest_cc_size(ugraph):
    """
    Takes an undirected graph and returns the integer 
    size of its largest connected component
    """
    connected_components = cc_visited(ugraph)
    if connected_components == []:
        return 0
    
    largest_component_size = max((len(component) \
                                  for component in connected_components))

    return largest_component_size


def compute_resilience(ugraph, attack_order):
    """
    Takes an undirected graph and a list of nodes attack_order; sequentially
    removes each node in attack_order (and its edges) from a copy of the graph
    and returns a list of the sizes of the largest remaining connected component
    in the copied graph after each node removal (leaves ugraph unmodified)
    """
    new_graph = copy_graph(ugraph)
    sizes = [largest_cc_size(new_graph)]
    
    for node in attack_order:
        neighbors = new_graph.pop(node, set([]))
        for neighbor in neighbors:
            new_graph[neighbor].remove(node)
        sizes.append(largest_cc_size(new_graph))

    return sizes

###############################################################################
# Application 2

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


def create_ER(num_nodes, prob):
    """
    Returns a dictionary representation a graph generated with the Erdos-Renyi
    algorithm, wherein each of the num_nodes nodes has a probability prob of
    sharing an edge with every other individual node (no parallel edges)
    """
    if prob < 0 or prob > 1:
        print "Error: prob must be a decimal in the interval [0, 1]"
        return {}
    
    er_graph = {}
    finished_nodes = set([])

    #initialize the dictionary
    for node in xrange(num_nodes):
        er_graph[node] = set([])
    
    for node in xrange(num_nodes):
        for potential_neighbor in xrange(num_nodes):
            if potential_neighbor not in finished_nodes \
             and node != potential_neighbor and prob > random.uniform(0, 1):
                er_graph[node].add(potential_neighbor)
                er_graph[potential_neighbor].add(node)
                
        finished_nodes.add(node)
             
    return er_graph


def create_UPA(num_nodes, edges_per_iter):
    """
    Generates a graph using UPA algorithm; num_nodes is a positive integer,
    edges_per_iter is a positive integer less than or equal to num_nodes
    """
    if edges_per_iter > num_nodes  or  num_nodes < 1 or edges_per_iter < 1:
        print "Invalid input passed to function create_UPA"
        return {}
    
    graph = make_complete_graph(edges_per_iter)
    node_pool = []
    for node in graph:
        node_pool.extend([node] * edges_per_iter)
    
    for node in xrange(edges_per_iter, num_nodes):
        new_neighbors = set()
        for dummy_idx in xrange(edges_per_iter):
            new_neighbors.add(random.choice(node_pool))
            
        graph[node] = new_neighbors
        for neighbor in new_neighbors:
            graph[neighbor].add(node)
            
        node_pool.extend(new_neighbors)
        node_pool.extend([node] * (1 + len(new_neighbors)))
        
    return graph

##########################################################
# Question 1: Graph resilience to random attacks

def random_order(graph):
    """
    Takes a dictionary representation of a graph; returns a list
    containing all nodes in the graph in a random order
    """
    order = graph.keys()
    random.shuffle(order)
    return order

network_graph = load_graph(NETWORK_URL)
# There are 1239 nodes and 3047 edges in the network graph.

er_graph = create_ER(len(network_graph), 0.003973)
# A graph with 1239 nodes generated with the ER algorithm is expected to have
#  3047 edges when probability p = 0.003973

upa_graph = create_UPA(len(network_graph), 3)
# A graph with 1239 edges generated with the UPA algorithm has approximately
#  3685 edges when the number of edges added per iteration (m) = 3.
#  m = 2 would also be acceptable for this analysis, but I will use m = 3.

network_attack_order = random_order(network_graph)
er_attack_order = random_order(er_graph)
upa_attack_order = random_order(upa_graph)

network_resilience_data = zip(range(1 + len(network_graph)), \
                        compute_resilience(network_graph, network_attack_order))

er_resilience_data = zip(range(1 + len(er_graph)), \
                    compute_resilience(er_graph, er_attack_order))

upa_resilience_data = zip(range(1 + len(upa_graph)), \
                     compute_resilience(upa_graph, upa_attack_order))


# I used the following code to export the plot data to CSV files
##np.savetxt('Network_Data.csv', \
##           [item for item in network_resilience_data], \
##           delimiter=',', fmt='%s')
##
##np.savetxt('ER_Data.csv', \
##           [item for item in er_resilience_data], \
##           delimiter=',', fmt='%s')
##
##np.savetxt('UPA_Data.csv', \
##           [item for item in upa_resilience_data], \
##           delimiter=',', fmt='%s')


# The three curves in the plot are all generally linear.

##########################################################
# Question 2: A quick analysis

# All three of the above graphs are resilient to random attacks
#  as the first 20% of their nodes are removed.

##########################################################
# Question 3: A more efficient function for generating a targeted attack
# order, and a runtime comparison between the two

def fast_targeted_order(ugraph):
    """
    Takes a dictionary representation of an undirected graph and
    returns a targeted attack order that prioritizes removing
    the remaining node with the highest degree
    
    More efficient than targeted_order
    """
    new_graph = copy_graph(ugraph)
    degree_sets = [set([]) for _ in new_graph]

    for node in new_graph:
        degree = len(new_graph[node])
        degree_sets[degree].add(node)

    attack_order = []
    
    for degree in xrange(len(new_graph) - 1, -1, -1):
        while len(degree_sets[degree]) != 0:
            node = random.choice(tuple(degree_sets[degree]))
            degree_sets[degree].remove(node)
            
            for neighbor in new_graph[node]:
                neighbor_degree = len(new_graph[neighbor])
                degree_sets[neighbor_degree].remove(neighbor)
                degree_sets[neighbor_degree - 1].add(neighbor)

            attack_order.append(node)
            delete_node(new_graph, node)

    return attack_order


def time_targeted_functions():
    """
    Returns a tuple containing two lists, which each contain tuples that
    represent the speed at which the functions targeted_order and
    fast_targeted_order (respectively) perform given different input sizes
    """
    slow_data = []
    fast_data = []
    
    for num_nodes in xrange(10, 1000, 10):
        
        graph = create_UPA(num_nodes, 5)
        
        slow_time1 = time.time()
        targeted_order(graph)
        slow_time2 = time.time()
        slow_data.append((num_nodes, slow_time2 - slow_time1))

        fast_time1 = time.time()
        fast_targeted_order(graph)
        fast_time2 = time.time()
        fast_data.append((num_nodes, fast_time2 - fast_time1))

    return (slow_data, fast_data)

slow_targeted_data, fast_targeted_data = time_targeted_functions()


# I again used numpy to export plot data to CSV files
##np.savetxt('Slow_Targeted_Data.csv', \
##           [item for item in slow_targeted_data], \
##           delimiter=',', fmt='%s')
##
##np.savetxt('Fast_Targeted_Data.csv', \
##           [item for item in fast_targeted_data], \
##           delimiter=',', fmt='%s')


# The function targeted_order is O(n^2)
# The function fast_targeted_order is O(n)

# The plot created with the above data is consistent
#  with my mathematical analysis of the algorithms.

##########################################################
# Question 4: Graph resilience to targeted attacks

network_targeted_order = targeted_order(network_graph)
er_targeted_order = fast_targeted_order(er_graph)
upa_targeted_order = fast_targeted_order(upa_graph)


network_targeted_res_data = zip(range(1 + len(network_graph)), \
                        compute_resilience(network_graph, network_targeted_order))

er_targeted_res_data = zip(range(1 + len(er_graph)), \
                    compute_resilience(er_graph, er_targeted_order))

upa_targeted_res_data = zip(range(1 + len(upa_graph)), \
                     compute_resilience(upa_graph, upa_targeted_order))


# I again used numpy to export plot data to CSV files
##np.savetxt('Network_Targeted_Data.csv', \
##           [item for item in network_targeted_res_data], \
##           delimiter=',', fmt='%s')
##
##np.savetxt('ER_Targeted_Data.csv', \
##           [item for item in er_targeted_res_data], \
##           delimiter=',', fmt='%s')
##
##np.savetxt('UPA_Targeted_Data.csv', \
##           [item for item in upa_targeted_res_data], \
##           delimiter=',', fmt='%s')

##########################################################
# Question 5: Another quick analysis

# Only the ER graph and UPA graph are resilient under targeted attacks as
#  the first 20% of their nodes are removed, as the size of their largest
#  remaining connected components at this point is within 25% of their
#  respective numbers of remaining nodes (although the UPA graph is nearly a
#  borderline case.) The network graph is not resilient under these conditions.

##########################################################
# Question 6: Practical application

# Between the two randomly generated graph types, I found ER graphs to be more
#  resilient than UPA graphs under targeted attacks. This can likely be
#  attributed to the way in which each edge generated in a UPA graph is biased
#  toward nodes that have already become more central (by gaining relatively
#  many edges), whereas with ER graphs the generation of an edge between any
#  two given nodes is equally probable.

# The random structure of an ER graph would certainly be an advantage when a
#  network is under attack, but this may not often be practical. A network with
#  any purpose other than to withstand attacks may require a more nuanced
#  structure. Of course, more otherwise unecessary connections (edges) could
#  be added to the network for improved resilience, but this may in turn lead
#  to greater implementation and maintenance costs.

###############################################################################

