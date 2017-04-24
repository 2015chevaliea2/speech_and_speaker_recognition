import unicodedata
import string
import re
import random
from class_lang import Lang
import numpy as np
from collections import Counter, OrderedDict
import anytree

# Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r"", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s

def readLangs(lang1, lang2, reverse=False):
    print("Reading lines...")

    # Read the file and split into lines
    lines = open('fra.txt', encoding = 'utf-8').read().strip().split('\n')
    
    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l.split('\t')][0] for l in lines]
    pairs = list(set(pairs))
    # Reverse pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)
        
    return input_lang, output_lang, pairs

def split_sentence(sentence):
    return(sentence.split(' '))

def split_txt():
    pairs = readLangs('ang', 'fra', reverse=False)[2]
    ans = []
    for i in range (len(pairs)):
        split = split_sentence(pairs[i])
        ans.append(split)
    return(ans)

#This function returns the list of distinct words as 1st argument, and the list of words with repetition as 2nd argument   
#def list_of_words(splitted_text):
#    words = []
#    for i in range(len(splitted_text)):
#        for j in range(len(splitted_text[i])):
#            words.append(splitted_text[i][j])
#    distinct_words = list(set(words))
#    N = len(distinct_words)
#    probabilities = np.zeros(N)
#    for i in range(N):
#        probabilities[i] = words.count(distinct_words[i])/len(words)
#    return(distinct_words,probabilities)
length = 100    
def language_dictionary(splitted_text):
    dictionary = Counter({})
    for i in range(length):
        dictionary = dictionary + Counter(splitted_text[i])
    return(dictionary,list(dictionary.keys()))
    
def SOS_EOS(splitted_text):
    with_SOS_EOS = splitted_text
    for i in range(len(splitted_text)):
        with_SOS_EOS[i] = ['SOS'] + with_SOS_EOS[i] + ['EOS']
    return(with_SOS_EOS)

def bigrams(splitted_text,L):
    N = len(dictionary)
    transition_mat = np.zeros((N,N))
    for i in range(length):
        sentence = splitted_text[i]
        for j in range(1,len(sentence)):
            previous_word = sentence[j-1]        
            current_word = sentence[j]
            line = L.index(previous_word)
            column = L.index(current_word)
            transition_mat[line,column] += 1 
    for i in range(N):
        transition_mat[i,:] = transition_mat[i,:]/np.sum(transition_mat[i,:])
    return(transition_mat)
                    
    

#pairs = readLangs('ang', 'fra', reverse=False)[2]
#s = split_sentence(pairs[])
splitted = split_txt()  
splitted2 = SOS_EOS(splitted)  
dictionary = language_dictionary(splitted2)[0]
L = language_dictionary(splitted2)[1]
M = bigrams(splitted2,L)

    
    
            
        










