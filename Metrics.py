from math import log
from wn_functions import *
import numpy


def metric(name, synset1, synset2,max_depth):
    

    if name == "Leakcock-Chodorow":
        """
        Implementation of the Leakcock-Chodorow metric.
        """
        
        len_s1_s2 = distance(synset1, synset2)
        if len_s1_s2 is None:
            return 0
        if len_s1_s2 == 0:  #aggiungiamo 1 al num e al den per evitare il log(0)
            len_s1_s2 = 1
            res = -(log((len_s1_s2 / ((2 * max_depth) + 1)), 10))
        else:
            res = -(log((len_s1_s2 / (2 * max_depth)), 10))
        return (res / (log(2 * max_depth + 1, 10))) * 10

    elif name == "Shortest-Path":
        """
        Implementation of the Shortest Path metric.
        """
       
        #print(max_depth) == 20 nella nostra versione di wordnet
        len_s1_s2 = distance(synset1, synset2)
        if len_s1_s2 is None:
            return 0
        res = 2 * max_depth - len_s1_s2
        return (res / (2 * max_depth)) * 10

    elif name == "Wu-Palmer":
        """
        Implementation of the Wu-Palmer metric.
        """
        lcs = lowest_common_subsumer(synset1, synset2)
        if lcs is None:
            return 0
        depth_lcs = depth_path(lcs, lcs)
        depth_s1 = depth_path(synset1, lcs)
        depth_s2 = depth_path(synset2, lcs)
        result = (2 * depth_lcs) / (depth_s1 + depth_s2)
        return result * 10 
    else:
        return


def pearson_index(x, y):
 
    # Implementation of the Pearson index.

    mu_x = numpy.mean(x)   #media degli score nella gold
    mu_y = numpy.mean(y)   #media degli score calc per una metrica
    std_dev_x = numpy.std(x)
    std_dev_y = numpy.std(y)

    modified__x = [elem - mu_x for elem in x]
    modified__y = [elem - mu_y for elem in y]

    num = numpy.mean(numpy.multiply(modified__x, modified__y)) # covariance
    denum = std_dev_x * std_dev_y # std_x * std_y

    return num / denum


def spearman_index(x, y):

    # Implementation of the Spearman index.
  
    rank__x = define_rank(x)
    rank__y = define_rank(y)

    return pearson_index(rank__x, rank__y)


def define_rank(x):
    
    # function that return the rank of a given vector

    x_couple = [(x[i], i) for i in range(len(x))]

    x_couple_sorted = sorted(x_couple, key=lambda x: x[0]) #sorta in base allo score (gold o algo)
    list_result = [y for (x, y) in x_couple_sorted]
    return list_result




    