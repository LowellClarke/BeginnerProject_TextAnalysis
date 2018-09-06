import string
import bisect
import random

def string_to_list(s):
    """Converts a string to a list of words

    s : string

    return : list
    """
    newlist = []
    
    words = s.split()

    for word in words:
        newlist.append(word.lower())

    return newlist
                                  
def markov_analysis(wordlist, n = 2):
    """Carries out markov analysis on a text and returns a map

    t : list of words
    n : sequence length
    
    return : map of sequences
    """

    #get tuple pairs/triplets/etc.
    
    tuples = []
    index = 0

        #Set slice for sequence length 1 (or 0)
    if n < 2:
        tslice = wordlist
    else:
        tslice = wordlist[:1-n]
    
    for word in tslice:
        #Get first word of tuple and add additional words based on n
        tup = (word,)
        for i in range(n-1):
            tup = tup + (wordlist[index + i + 1],)
        tuples.append(tup)
        index += 1

    #Create frequency mapping
    index = 0
    full_map = {}

        #For each pair
    for tup in tuples:
        index = 0
        fmap = {}
            #For each word that comes after each pair
        for word in wordlist[n:]:
            count = 0
            for j in range(n):
                if wordlist[index + j] == tup[j] :
                    count += 1
                if count == n:
                    fmap[word] = fmap.get(word, 0) + 1
            index += 1
        full_map[tup] = fmap

    return full_map

def choose_from_hist(hist):
    """From a histogram / mapped dictionary containing frequencies of the key,
    this function randomly returns one key from the mapped dictionary.

    hist : histogram

    return : string
    """
    prob = []
    letter = []

    total = 0
    for item, value in hist.items():
        letter += [item]
        total += value
        prob += [total - 1]
  
    choice = random.randint(0, total-1)
    i = bisect.bisect_left(prob, choice)
    
    return letter[i]

def print_markov(word_list, n = 2):
    """Uses a markov mapping to proceedurally
    generate a similar piece of writing

    word_list : list of strings

    return : printed string  
    """

    #Get markov histogram
    markov_map = markov_analysis(word_list, n)
    
    #Get first n words of writing to start
    writing = []
    for i in range(n):
        writing.append(word_list[i])

    
    iter = 0
    while True:        
        #Get index slice for preceeding words
        preceeding = ()
        for i in range(n):
            preceeding = preceeding + (writing[i + iter],) 

        #Retrieve histogram relating to preceeding words
        hist = markov_map[preceeding]

        
        try:
            #Pick one random word from histogram 
            choice = choose_from_hist(hist)
            writing.append(choice)
            iter += 1
            #And reiterate for next set of two words
        except:
            #When the last words of the sequence are reached
            print()
            break
            

    for word in writing:
        print(word, end = ' ')
    

def main():
    test_string = ' Half a bee, philosophically, \n Must, ipso facto, half not be. \n But half the bee has got to be \n Vis a vis, its entity. D’you see? \n But can a bee be said to be \n Or not to be an entire bee \n When half the bee is not a bee \n Due to some ancient injury?'
    #test_string = ' Half a bee, philosophically, \n Must, ipso facto, half not be.'
    
    #Strip Punctuation from string
    test_string = test_string.translate(str.maketrans('','', string.punctuation))
    
    #Get list of words
    t = string_to_list(test_string)

    #Repeat the generation for different sequence lengths
    
    for n in range(5):
        print("\n")
        print("Bee poem at sequence length %s" %(n+1))
        print_markov(t, n+1)

        #Sequence length determines how many words are stored in
        #a dictionary agaisnt a single word that comes after them

if __name__ == '__main__':
    main()
