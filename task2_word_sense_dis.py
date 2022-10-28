from lxml import etree as Exml
from tqdm import tqdm
import random
import os
import re
import sys
import xml.etree.ElementTree as ET
from lesk_imp import *



input = os.path.dirname(__file__) + '/input/semcor3.0/brown1/tagfiles/br-a01'
output = os.path.dirname(__file__) + '/output/'


def parseXML(path):

    #It parses the SemCor corpus, which has been annotated by hand on WordNet Sysnsets. [(sentence, [(word, gold)]),...]
  
    with open(path, 'r') as fileXML:
        # Load XML file (root, paragraphs and words)
        file = fileXML.read()
        file = file.replace('\n', '')
        replacer = re.compile("=([\w|:|\-|$|(|)|']*)")
        file = replacer.sub(r'="\1"', file) # \1 is the replacement to use in case of a match, so that a repeated word will be replaced by a single word.
        result = []
        try:
            root = Exml.XML(file)
            paragraphs = root.findall("./context/p")
            sentences = []
            # Took all the tags "s" (substantive)
            for p in paragraphs:
                sentences.extend(p.findall("./s"))
            # Extract the sentence
            for s in sentences:
                words = s.findall('wf')
                phrase = ""
                tuple_list = [] # list of all the tuple ((word, gold_sense/wnsn in SemCore))
                # Select the words to disambiguate (select only the needed ones, which have multiple senses)
                for word in words:
                    w_text = word.text
                    tag = word.attrib['pos'] #search POS tagging attribute of word
                    phrase = phrase + w_text + ' ' # string containing all the words parsed in the sentences (for all paragraph)
                    # if word's POS tag attribute is "NN" = substantive and word have multiple senses and WordNet synsets attribute for word exists 
                    if tag == 'NN' and '_' not in w_text and len(wn.synsets(w_text)) > 1 and 'wnsn' in word.attrib: # wnsn = WordNet synset annotated in the SemCor corpus as the "gold" sense
                        sense = word.attrib['wnsn']
                        t = (w_text, sense) # tuple (word, gold_sense)
                        tuple_list.append(t) # building the list of all the tuple considered
                result.append((phrase, tuple_list)) # adding the tuple relative to the paragraph p just parsed
        except Exception as e:
            raise NameError('xml: ' + str(e))
    return result # a list of tuple [ ("string_all_parsed_words_in_sentences", [(word1,wnsn), (word2, wnsn), (...),...]), (...), ...] ) ]
                  # with one tuple for each paragraph parsed in SemCor corpus

    
def W_Sense_Disambiguation():

    # Extracts sentences from the SemCor corpus (corpus annotated with WN synset) and disambiguates at least 
    # one ambiguous noun (words with POS_tag 'NN' and multiple WN synsets) per sentence.
    

    parse_xml = parseXML(input)

    indexes = random.sample(range(0, len(parse_xml)-1),50) # extract 50 random sentences from the SemCor corpus parsed (randomize tuple choice in result)

    c_word = 0
    c_found = 0
    result = []
    
    for i in indexes:
        if len(result) < 50:
            dict_list = []
            sentence = parse_xml[i][0] # i^ paragraph, first elem of the result tuple (sent) = " sent + w + ' ' "
            # randomize the choosing of t (the substantive to disambiguate among the t words)
            word_gold = parse_xml[i][1]  # i^ paragraph, second elem of the result tuple (tuple_list) = [(word1,wnsn), (word2,wnsn), (...)]
            if len(word_gold) != 0:
                indexes_word = random.randrange(0, (len(word_gold)))
                
                tuple_word = word_gold[indexes_word]
                word = tuple_word[0]
                wnsn = tuple_word[1] # second elem of the tuple t (words) = wnsn (gold_score)

                sense = lesk_alghoritm(word, sentence)  # running lesk's algorithm on word t[0] and its context sentence
                                                       # -> returns its best sense in context
                w_sense_index = str(get_sense_index(word, sense)) # returning index (among the WN synsets list) of the word sense just found
                
                c_word += 1
                if wnsn == w_sense_index:
                    c_found += 1
                dict_list.append({'word': word, 'gold': wnsn, 'value': w_sense_index}) # {1: word, 2: wnsn/golden_sense, 3: lesk_sense}

                if len(dict_list) > 0:
                    result.append((sentence, dict_list)) # [ (word_context, word_evaluation/dict_list), ... ]
                
            else: # empty 
                i = i + 1
    
    accuracy = c_found / c_word      # correct / total 

    return accuracy, result




def write_output_to_csv(accuracy, result):
    
    # Writes the output into a csv file.
    
    with open(output + 'ws_disambiguation_results.csv', "a") as out:
        for j in range(len(result)):
            out.write(f"sentence_number: {j + 1}  ")
            out.write(result[j][0] + "\n")
            for word in result[j][1]: # word_evaluation
                out.write(f"Word: {word['word']},  ")
                out.write(f"Gold: {word['gold']},  ")
                out.write(f"Value: {word['value']}\n")
            
        out.write(f"Accuracy: {accuracy}\n\n\n")



if __name__ == "__main__":
    with open(output + 'ws_disambiguation_results.csv', "w") as out:
        out.write("")
    print("\nWord Sense Disambiguation TASK :\n ")
    avg = 0
    for i in range (1,11):
        print(f"{i}° Iteration - Lesks's algorithm")
        acc, res = W_Sense_Disambiguation()
        write_output_to_csv(acc,res)
        avg += acc

    print(f"Average Accuracy: {avg/10} ")

