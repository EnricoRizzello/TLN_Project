from wn_functions import *
import time
import os
from Metrics import *

output = os.path.dirname(__file__) + '/output/'
input = os.path.dirname(__file__) + '/input/'

def wsim353_parse(path):
    result = []
    with open(path, 'r') as file:
        for line in file.readlines()[1:]:
            ar = line.split(",")
            score = ar[2].replace('\n', '')
            result.append((ar[0], ar[1], float(score)))

    return result



def compute(metric_name,parse_result,max_depth):
    
    rem = []
    count_senses = 0  # to count the senses total
    
    sim_metric = []  # similarity list for this metric

    j = 0
    for couple_terms in parse_result:
        syn1 = get_synsets(couple_terms[0])
        syn2 = get_synsets(couple_terms[1])
        # senses = [synset1, synset2]

        max_sim = []  # list of senses similarity between the two senses considered at each time
        for s1 in syn1:
            for s2 in syn2:
                count_senses += 1
                max_sim.append(metric(metric_name,s1, s2,max_depth)) # tutte le misure di similarità considerate per ogni senso di ogni couple_terms
        if len(max_sim) == 0:  # word without senses (ex.: proper nouns)
            max_sim = [-1]
            rem.append(j)
        sim_metric.append(max(max_sim)) # massime similarità per ogni couple_terms
        j += 1
    return sim_metric, rem, count_senses

def cs_task():


    parse_result = wsim353_parse(input + "WordSim353.csv")
    print(f"--- WordSim353.csv parsed. ")

    max_depth = depth_max()
    
    max_similarities = []  # lista di liste (una per ogni couple_terms) di similarità, una lista per ogni metric
    Total_Senses = 0
  

    n_ms = ["Wu-Palmer","Shortest-Path","Leakcock-Chodorow"]
    for m in n_ms:
        sm,toremove,cs = compute(m,parse_result,max_depth)
        print(f"--- Compute max Similarity score using {m}'s metric.")
        max_similarities.append(sm)
        Total_Senses += cs

    for j in range(len(parse_result)):
        if j in toremove:
            del parse_result[j]
            for s in range(len(max_similarities)):
                del max_similarities[s][j]
    
    
    print(f"----- Total senses similarity: {Total_Senses}")

    
    gold = [elem[2] for elem in parse_result]  # the list of golden annotations (scores column)

    pearson = []
    spearman = []

    for i in range(3):
        ms = max_similarities[i] # similarity list associata alla singola misura ogni volta
        pearson.append(pearson_index(gold, ms))
        spearman.append(spearman_index(gold, ms))

    with open(output + 'results.csv', "w") as out:
        out.write(f"word1, word2, Wu-Palmer, Shortest-Path, Leakcock-Chodorow, gold\n")
        for j in range(len(parse_result)):
            out.write("{0}, {1}, {2:.2f}, {3:.2f}, {4:.2f}, {5}\n".format(parse_result[j][0], parse_result[j][1], max_similarities[0][j],
                        max_similarities[1][j], max_similarities[2][j], parse_result[j][2]))

    with open(output + 'correlation_indices.csv', "w") as out:
        out.write("Metric , Pearson, Spearman\n")
        out.write(f"Wu-Palmer, {str(pearson[0])}, {spearman[0]}\n")
        out.write(f"Shortest-Path, {str(pearson[1])}, {spearman[1]}\n")
        out.write(f"Leakcock-Chodorow, {str(pearson[2])}, {spearman[2]}\n")


if __name__ == "__main__":

    """ execute the conceptual similarity task """
    cs_task()