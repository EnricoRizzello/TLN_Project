import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords



def bag_of_word(sentence):
   
    # Transforms the sentence in input according to the bag of words approach, apply lemmatization, stop words and punctuation removal.

    # bow = an unordered set of words, ignoring their exact position
    list_tokens = []
    stop_words = set(stopwords.words('english'))
    punctuation = {',', ';', '(', ')', '{', '}', ':', '?', '!'}
    wnl = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(sentence)
    
    for t in tokens:
        if t not in stop_words and t not in punctuation:
            list_tokens.append(t)

    return set(wnl.lemmatize(t) for t in list_tokens)


def compute_overlap(signature, context):

    #Computes the number of words incommon between signature and context.
    return len(signature & context)




def lesk_alghoritm(word, sentence):

    #Lesk's algoritm implementation. Given a word and a sentence in which it appears, it returns the best sense of the word.
    

    # Calculating the synset of the given word inside WN
    word_senses = wn.synsets(word)
    best_sense = word_senses[0] #most frequent sense for word
    max_overlap = 0

    # The simplest bag-of-words approach represents the context of a target word by a vector of features,
    # each binary feature indicating whether a vocabulary word w does or doesn’t occur in the context.
    context = bag_of_word(sentence) # set of words in sentence

    for sense in word_senses:
        # set of words in the gloss
        signature = bag_of_word(sense.definition())

        # and examples of the given sense
        examples = sense.examples()
        for ex in examples:
            # after this line, signature will contain for all the words, their
            # bag of words of (sense definition + sense examples)
            signature = signature.union(bag_of_word(ex))

        overlap = compute_overlap(signature, context)
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense

    return best_sense


def get_sense_index(word, sense):

    #it returns the corresponding index of the sense in the synsets list associated with the word indices, that starts with 1.
    senses = wn.synsets(word)
    return senses.index(sense) + 1

