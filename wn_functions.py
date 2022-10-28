from nltk.corpus import wordnet as wn



def depth_path(synset, lcs):
        
        #It mesures the distance (depth) between the given Synset and the WordNet's root.
 
        list_path = []
        paths = synset.hypernym_paths() #lista di tutti i possibili cammini dalla radice all'synset

        for p in paths:
            if lcs in p:
                list_path.append(p)

        return min(len(path) for path in list_path)

def lowest_common_subsumer(synset1, synset2):

        #function that return the first common subsumer between the synset in input
        if synset1 == synset2:
            return synset1

        commons = []
        for h in synset1.hypernym_paths():  #for each paths
            for k in synset2.hypernym_paths():
                zipped = list(zip(h, k))  # merges 2 list of paths in one list of tuples
                common = None
                for i in range(len(zipped)):
                    if zipped[i][0] != zipped[i][1]: #[(i 0, i 1), (,) .....]
                        break
                    common = (zipped[i][0], i)

                if common is not None and common not in commons:
                    commons.append(common)

        if len(commons) <= 0:
            return None
    
        commons.sort(key=lambda x: x[1], reverse=True) #sorta in base all'indice i delle tuple common inserite in commons 
        return commons[0][0]

def distance(synset1, synset2):
        
        # function that return the distance between the two synset
       

        lcs = lowest_common_subsumer(synset1, synset2)
        lists_synset1 = synset1.hypernym_paths()
        lists_synset2 = synset2.hypernym_paths()

        if lcs is None:
            return None

        # path from LCS to root (to exclude in the comparison between the 2 synsets)
        lists_lcs = lcs.hypernym_paths()

        set_lcs = set()
        for l in lists_lcs:  
            for i in l:      # nodes
                set_lcs.add(i)
        set_lcs.remove(lcs)  # nodes from LCS (not included) to root
        
        # path from synset to LCS (recude paths to check, within LCS)
    
        lists_synset1 = list(map(lambda x: [y for y in x if y not in set_lcs], lists_synset1))
        lists_synset2 = list(map(lambda x: [y for y in x if y not in set_lcs], lists_synset2))
        
        # path containing LCS
        lists_synset1 = list(filter(lambda x: lcs in x, lists_synset1))
        lists_synset2 = list(filter(lambda x: lcs in x, lists_synset2))

        return min(list(map(lambda x: len(x), lists_synset1))) + min(list(map(lambda x: len(x), lists_synset2))) - 2


def depth_max():

    #function that return the length of the longest hypernym path from this synset to the root.
    return max(max(len(path) for path in sense.hypernym_paths()) for sense in wn.all_synsets())

 
def get_synsets(word):
        
    #function that return the Synset list associated to the given word
    return wn.synsets(word)
