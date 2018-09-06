import string
from bisect import bisect_left
from random import randint

def striplist(t):
    """Takes a word file in list format and
    returns a list of all the words.

    t : list of strings
    
    return : list of strings
    """
    
    newlist = []

    #Traverse list of lines
    for line in t:
        #Strip punctation and whitespace
        line = line.replace('—', ' ').translate(str.maketrans('','',string.punctuation + '“”’‘1234567890'))
        words = line.split()
        #Append indivdual words to a new list
        for word in words:
            newlist.append(word.lower())

    return newlist

def worduse(t):
    """Takes a list of strings and returns a
    dictionary of the occurance of each word
    
    t : list of strings
    
    return : dictionary    
    """
    
    d = {}
    
    for word in t:
        if word not in d:
            d[word] = 1
        else:
            d[word] += 1

    return d

def topwords(t):
    """Takes a list of strings and
    returns the top occuring words

    t : list

    return : sorted list of tuples (word, count)
    """

    d = worduse(t)

    #convert to tuple list
    t_l = [(k,v) for k,v in d.items()]
    #Sort list highest to lowest
    t_l.sort(key=lambda x: x[1], reverse = True)

    return t_l
    
def print_topwords(wordlist, n = 20):
    """Prints information about a word list's top words"""
    
    top = topwords(wordlist)
    
    for word,v in top[:n]:
        buffer = len(str(len(wordlist))) - 1
        disp_value = str(v) + int(buffer - len(str(v)))*' '
        print(disp_value, word)

def not_in_dict(wordlist):
    """Checks to see if words in a word list are in an
    existing file/word list and returns those that are not

    wordlist : list of words

    returns : list of words        
    """
    dictionary = {'a' : None, 'i' : None}
        
    with open('words.txt', "r") as dfile: 
        for line in dfile:
            word = line.strip()
            dictionary[word] = None
            
    weirdwords = []
    
    for word in wordlist:
        if word not in dictionary:
            weirdwords.append(word)

    return weirdwords

def rand_word(hist):
    """Chooses a random word from a histogram

    The likelihood of each word is proportional to its frequency

    hist : map of words to their frequency

    return : one random word string
    """

    #initial sets and values
    prob = []
    word = []
    total = 0

    #create cumulative values from histogram
    for item, value in hist.items():
        word += [item]
        total += value
        prob += [total - 1]

    #pick a random number and retrieve index
    choice = randint(0, total-1)
    index = bisect_left(prob, choice)

    #return word at index
    return word[index]
    
def print_rand_words(wordlist, n):
    """Takes a list of word and returns words from it

    return : word list of length n
    """
    chosen = []

    #Generates words and avoids duplicates
    while len(chosen) < n:
        chosenword = rand_word(worduse(wordlist))
        if chosenword not in chosen:
            chosen.append(chosenword)

    #Prints generated words

    print("\nHere are %s words chosen randomly in proportion to their frequency:"
          %(n), end = "\n  ")

    for word in chosen[:-2]:
        print(word, end = ', ')
    print(chosen[-2], "and", chosen[-1])
    

def words_from_file(file_name):
    """Opens file name and returns a list of lines of words

    file_name : file name string

    returns : lines from file as strings in list
    """
    
    with open(file_name, "r") as lst:
        words = []
        for line in lst:
            word = line.strip()
            words.append(word)
        return words

def get_wordlist():
    """Asks for user input for a file name, opens the file
    and returns all the words in that file as a list.

    If the file name is invalid, mobydick.txt will be used instead

    returns : list of words, file name string
    """
    try:
        #Ask user for input
        file_name = input("What text file would you like to analyse?")
        wordlist = striplist(words_from_file(file_name))
    except:
        #If name invalid, uses mobydick.txt
        print("File not found, using mobydick.txt instead")
        file_name = "mobydick.txt"
        wordlist = striplist(words_from_file(file_name))
    print()
    return wordlist, file_name

def print_info(wordlist, file_name = 'Text doc'):
    """ForPrints word count, unique word count,
    list of top words and list of unrecognised words

    wordlist : list of words
    file_name : file name string
    """
    #Print General Info
    print("%s has\n  %s words and %s unique words"
          %(file_name, len(wordlist), len(topwords(wordlist))))
    #Print Top word list
    print("\nTop words are:")
    print_topwords(wordlist)

    #Print Unusual word list
    topweird = not_in_dict(wordlist)
    print("\nTop words not in dictionary are:")
    print_topwords(topweird)

def main():
    wordlist, file_name = get_wordlist()
    print_info(wordlist, file_name)
    print_rand_words(wordlist, 10)

if __name__ == '__main__':
    main()

