"""
Algorithmic Thinking: Project 3
(Rice University)

Student: Jared Cooney
jaredcooney2@gmail.com

View all the images generated in this project here:
https://www.dropbox.com/sh/c49vjvlcv8j0foc/AAD8ca115EFMbRdV7uMa_Zm-a?dl=0

=============================================================
Project Instructions:

    Implement the following functions:

    slow_closest_pair(cluster_list)
    fast_closest_pair(cluster_list)
    closest_pair_strip(cluster_list, horiz_center, half_width)
    hierarchical_clustering(cluster_list, num_clusters)
    kmeans_clustering(cluster_list, num_clusters, num_iterations)

    where cluster_list is a 2D list of clusters in the plane
"""

import math
import urllib2
import alg_cluster

######################################################
# Code for loading the given cancer risk data

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
##    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


data_111_table = load_data_table(DATA_111_URL)
data_290_table = load_data_table(DATA_290_URL)
data_896_table = load_data_table(DATA_896_URL)
data_3108_table = load_data_table(DATA_3108_URL)


def create_singleton_list(data_table):
    """Takes a data table and converts it to a list of singleton clusters"""
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], \
                                                  line[2], line[3], line[4]))
    return singleton_list

######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function; computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and
    idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), \
            min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist      
    """
    closest_info = (float("inf"), -1, -1)

    for cluster1_idx in xrange(len(cluster_list)):  
        for cluster2_idx in xrange(len(cluster_list)):

            if cluster1_idx != cluster2_idx:
                pair_info = pair_distance(cluster_list, \
                                           cluster1_idx, cluster2_idx)
                
                closest_info = min(closest_info, pair_info, key=lambda x: x[0])
    
    return closest_info


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal
    positions of their centers are in nondecreasing order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist      
    """
    list_size = len(cluster_list)

    # base case
    if list_size <= 3:
        return slow_closest_pair(cluster_list)

    # recursive case
    mid_idx = list_size // 2
    left = cluster_list[: mid_idx]
    right = cluster_list[mid_idx :]

    left_closest = fast_closest_pair(left)
    right_closest = fast_closest_pair(right)
    right_closest = (right_closest[0], \
                     right_closest[1] + mid_idx, right_closest[2] + mid_idx)

    closest_info = min(left_closest, right_closest, key = lambda info: info[0])
    
    mid_xval = 0.5 * (cluster_list[mid_idx - 1].horiz_center() + \
                      cluster_list[mid_idx].horiz_center())

    strip_info = closest_pair_strip(cluster_list, mid_xval, closest_info[0])
    closest_info = min(closest_info, strip_info, key = lambda info: info[0])
    
    return closest_info


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function; computes the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal
    distance that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the
    centers of the clusters cluster_list[idx1] and cluster_list[idx2]
    lie in the strip and have minimum distance dist
    """
    strip_idcs = [idx for idx in xrange(len(cluster_list)) \
                  if abs(cluster_list[idx].horiz_center() - horiz_center) \
                                                            < half_width]
    
    strip_idcs.sort(key = lambda idx: cluster_list[idx].vert_center())
    
    list_size = len(strip_idcs)
    closest_info = (float("inf"), -1, -1)
    
    for cluster1_idx in xrange(list_size - 1):
        for cluster2_idx in xrange(cluster1_idx + 1, \
                                   min(cluster1_idx + 4, list_size)):

            new_pair_info = pair_distance(cluster_list,
                                          strip_idcs[cluster1_idx], 
                                          strip_idcs[cluster2_idx])
            
            closest_info = min(closest_info, new_pair_info, \
                               key = lambda info: info[0])

    return closest_info


######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Mutates cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        closest_pair_info = fast_closest_pair(cluster_list)
        
        idx1 = closest_pair_info[1]
        idx2 = closest_pair_info[2]
        cluster1 = cluster_list[idx1]

        cluster1.merge_clusters(cluster_list.pop(idx2))

    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Does not mutate cluster_list
    
    Input: List of clusters, integers number of clusters & number of iterations
    Output: List of clusters whose length is num_clusters
    """
    
    # initial "centers" are placed at locations of highest population clusters
    old_clusters = []
    pop_sorted_clusters = sorted(cluster_list, reverse = True,
                               key = lambda cluster: cluster.total_population())
    for idx in xrange(num_clusters):
        old_clusters.append(pop_sorted_clusters[idx])
        

    # refine the clustering to be more accurate with each iteration
    for dummy_iteration in xrange(num_iterations):
        
        new_clusters = []
        for dummy_idx in xrange(num_clusters):
            new_clusters.append(alg_cluster.Cluster(set([]), 0, 0, 0, 0))

        for idx in xrange(len(cluster_list)):
            closest_old = (float("inf"), None)
            for old_idx in xrange(len(old_clusters)):
                distance = cluster_list[idx].distance(old_clusters[old_idx])
                if distance < closest_old[0]:
                    closest_old = (distance, old_idx)

            new_clusters[closest_old[1]].merge_clusters(cluster_list[idx])

        old_clusters = new_clusters

    return new_clusters


###############################################################################
###############################################################################
# Application 3

import time
import random
import numpy as np

##########################################################
# Question 1: Comparing the runtimes of the slow and fast closest pair functions

def gen_random_clusters(num_clusters):
    """
    Takes a positive integer number of clusters to be generated, returns 
    a list of clusters that each correspond to a randomly generated point 
    in the square with edge lenght 2 centered about the origin
    """
    clusters = []
    for dummy_idx in xrange(num_clusters):
        x_coord = 2 * random.random() - 1
        y_coord = 2 * random.random() - 1
        new_cluster = alg_cluster.Cluster(set([]), x_coord, y_coord, 0, 0)
        clusters.append(new_cluster)
        
    return clusters

        
def time_pair_functions():
    """
    Returns a tuple containing two lists, which each contain tuples that
    represent the speed at which the functions slow_closest_pair and
    fast_closest_pair (respectively) perform given different input sizes
    """
    slow_data = []
    fast_data = []
    
    for cluster_size in xrange(2, 201):
        cluster_list = gen_random_clusters(cluster_size)
        
        slow_start_time = time.time()
        slow_closest_pair(cluster_list)
        slow_end_time = time.time()
        slow_data.append((cluster_size, slow_end_time - slow_start_time))

        fast_start_time = time.time()
        fast_closest_pair(cluster_list)
        fast_end_time = time.time()
        fast_data.append((cluster_size, fast_end_time - fast_start_time))

    return (slow_data, fast_data)

slow_pair_data, fast_pair_data = time_pair_functions()


# I used numpy to export plot data to CSV files
##np.savetxt('Slow_Pair_Data.csv', \
##           [item for item in slow_pair_data], \
##           delimiter=',', fmt='%s')
##
##np.savetxt('Fast_Pair_Data.csv', \
##           [item for item in fast_pair_data], \
##           delimiter=',', fmt='%s')

# View the resulting runtime comparison plot here:
# https://www.dropbox.com/s/jhzxletbji8bstk/ClosestPairRuntimePlot.png?dl=0

##########################################################
# Question 2: Using hierarchical_clustering to create 15 clusters 
#             from the given 3108-county cancer risk data

# View the image (generated using the provided visualization tool) here:
# https://www.dropbox.com/s/xoiw9xy7e6ywuyi/Hier3108_15Clusters.png?dl=0

##########################################################
# Question 3: Using kmeans_clustering to create 15 clusters from the 
#             given 3108-county cancer risk data (with 5 iterations)

# View the image (generated using the provided visualization tool) here:
# https://www.dropbox.com/s/wbwcyse6zmbz6os/KMeans3108_15Clusters.png?dl=0

##########################################################
# Question 4: Efficiency comparison between clustering algorithms

# K-Means Clustering is a more efficient algorithm than Hierarchical
#  Clustering when the number of clusters created is a small constant
#  or small fraction of the number of input clusters.

# Under these circumstances, K-Means Clustering is simply O(n), meanwhile
#  Hierarchical Clustering is O(n^2 * log^2(n))

##########################################################
# Question 5: Using hierarchical_clustering to create 9 clusters 
#             from the given 111-county cancer risk data

q5_singleton_list = create_singleton_list(data_111_table)
question5_clustering = hierarchical_clustering(q5_singleton_list, 9)

# View the image (generated using the provided visualization tool) here:
# https://www.dropbox.com/s/r890x4nx22ux9c6/Hier111_9Clusters.png?dl=0

##########################################################
# Question 6: Using kmeans_clustering to create 9 clusters from the 
#             given 111-county cancer risk data (with 5 iterations)

q6_singleton_list = create_singleton_list(data_111_table)
question6_clustering = kmeans_clustering(q6_singleton_list, 9, 5)

# View the image (generated using the provided visualization tool) here:
# https://www.dropbox.com/s/46t9806vxkuyyc4/KMeans111_9Clusters.png?dl=0

##########################################################
# Question 7: Cluster error and clustering distortion

def compute_distortion(cluster_list, data_table):
    """
    Takes a clustering cluster_list of the given cancer risk data table and
    returns its distortion (the sum of the errors of each constituent cluster)
    """    
    distortion = 0
    for cluster in cluster_list:
        error = cluster.cluster_error(data_table)
        distortion += error

    return distortion

        
question5_distortion = compute_distortion(question5_clustering, data_111_table)
print "Distortion of the hierarchical clustering of 111 counties " + \
       "into 9 clusters:\n" + str(question5_distortion) + "\n"

question6_distortion = compute_distortion(question6_clustering, data_111_table)
print "Distortion of the k-means clustering of 111 counties into " + \
       "9 clusters using 5 iterations:\n" + str(question6_distortion) + "\n"


# The hierarchical clustering from question 5 has distortion 1.7516 * 10^11
# The k-means clustering from question 6 has distortion 2.7125 * 10^11

##########################################################
# Question 8: Comparing the clusterings from the previous questions

# K-Means Clustering produced a clustering with much higher distortion 
#  than Hierarchical Clustering.
#  Arguably the "worst" clusters in the k-means clustering are the one including
#  counties in Arizona and Colorado as well the one including counties in
#  California and the Pacific northwest. This can be explained by thinking about
#  how the United States population density map interacts with the k-means
#  clustering algorithm.

# K-means clustering chooses the counties with the highest populations as its
#  initial cluster center locations, then refines those center locations
#  using the locations of the nearest clusters. The western United States has
#  relatively few highly-populated cities compared to the eastern half of the
#  country, and several of the ones it does contain are relatively close
#  together (in California). The algorithm thus initialized with too few
#  cluster centers near the west coast, and most of them were bunched in the
#  same general area instead of being spread evenly across the coast, so
#  they had sets of nearest counties that were very far apart from each other.
#  The subsequent refining iterations did not "fix" this problem due to the
#  sparse population of that area of the country.

##########################################################
# Question 9: Automation

# Hierarchical Clustering clearly requires less human supervision to produce
#  a relatively low-distortion clustering. In contrast, K-Means Clustering 
#  produces different results depending on how it is programmed to choose its
#  initial cluster center locations, and some results will be better than
#  others.

##########################################################
# Question 10: Computing distortions for hierarchical and k-means 
#              clusterings of the 111, 290, and 896 county data sets,  
#              with the number of clusters ranging from 6 to 20

data_tables = (data_111_table, data_290_table, data_896_table)

# compute k-means distortions
kmeans_distortions = []
for idx in xrange(len(data_tables)):
    kmeans_distortions.append([])
    singleton_list = create_singleton_list(data_tables[idx])
    for num_clusters in xrange(6,21):
        new_clustering = kmeans_clustering(singleton_list, num_clusters, 5)
        distortion = compute_distortion(new_clustering, data_tables[idx])
        kmeans_distortions[idx].append((num_clusters, distortion))

kmeans_111_distortions = kmeans_distortions[0]
kmeans_290_distortions = kmeans_distortions[1]
kmeans_896_distortions = kmeans_distortions[2]


#compute hierarchical distortions
hierarchical_distortions = []
for idx in xrange(len(data_tables)):
    hierarchical_distortions.append([])
    clustering = create_singleton_list(data_tables[idx])
    for num_clusters in xrange(20, 5, -1):
        hierarchical_clustering(clustering, num_clusters)
        distortion = compute_distortion(clustering, data_tables[idx])
        hierarchical_distortions[idx].append((num_clusters, distortion))
        
    hierarchical_distortions[idx].reverse()

hier_111_distortions = hierarchical_distortions[0]
hier_290_distortions = hierarchical_distortions[1]
hier_896_distortions = hierarchical_distortions[2]


# I again used numpy to export plot data to CSV files
##np.savetxt('hier_111_distortions.csv', \
##           [item for item in hier_111_distortions], \
##           delimiter=',', fmt='%s')
##np.savetxt('hier_290_distortions.csv', \
##           [item for item in hier_290_distortions], \
##           delimiter=',', fmt='%s')
##np.savetxt('hier_896_distortions.csv', \
##           [item for item in hier_896_distortions], \
##           delimiter=',', fmt='%s')
##np.savetxt('kmeans_111_distortions.csv', \
##           [item for item in kmeans_111_distortions], \
##           delimiter=',', fmt='%s')
##np.savetxt('kmeans_290_distortions.csv', \
##           [item for item in kmeans_290_distortions], \
##           delimiter=',', fmt='%s')
##np.savetxt('kmeans_896_distortions.csv', \
##           [item for item in kmeans_896_distortions], \
##           delimiter=',', fmt='%s')


# View the plot images generated from this data here:

#    111-county distortion data
#    https://www.dropbox.com/s/ttk0kgbuf3rbafo/DistortionPlot111.png?dl=0

#    290-county distortion data
#    https://www.dropbox.com/s/ypgstzze4tj0lnt/DistortionPlot290.png?dl=0

#    896-county distortion data
#    https://www.dropbox.com/s/mdk29bvd4504lfi/DistortionPlot896.png?dl=0

##########################################################
# Question 11: Clustering algorithm distortion comparison when   
#              the number of clusters is in the range 6 to 20

# For the 111-county data set, Hierarchical Clustering consistently produces
#  less distorted clusterings than K-Means Clustering.

# For the 290-county data set, Hierarchical Clustering produces slightly less
#  distorted clusterings than K-Means Clustering for most values of the number
#  of clusters. However, there are several exceptions, and overall the 
#  difference is relatively small.

# For the 896-county data set, neither algorithm is clearly superior 
#  to the other in terms of clustering distortion.

##########################################################
# Overall Evaluation

# The hierarchical clustering algorithm has a much slower runtime than the
#  k-means clustering algorithm, but it tends to produce less distorted
#  clusters when the data set is small or when many of the most heavily-
#  weighted data points are relatively close together. This algorithm is
#  therefore also preferable when automation is important, as its output does
#  not depend on the placement of an initial group of cluster centers,
#  unlike k-means clustering.

# The k-means clustering algorithm is preferable when the data set is large
#  and relatively homogenously weighted, or when the situation allows for a
#  human operator to manually select the locations of the initial
#  clusters centers. Additionally, a large enough data set will render
#  hierarchical clustering infeasible due to a prohibitively high runtime.

