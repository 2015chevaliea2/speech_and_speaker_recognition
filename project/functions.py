import unicodedata
import re
import random
from class_lang import Lang
import numpy as np
from collections import Counter, OrderedDict
import copy

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

    
def language_dictionary(splitted_text,length):
    dictionary = Counter({})
    for i in range(length):
        dictionary = dictionary + Counter(splitted_text[i])
    return(dictionary,list(dictionary.keys()))

# Input : a dictionary retrned by language_dictionary[0]
def language_dictionary_UNK(dictionary):
    dictionary_UNK = {'UNK' : 0}
    for i in dictionary.keys():
        if dictionary[i] > 1:
            dictionary_UNK[i] = dictionary[i]-1
        dictionary_UNK['UNK'] = dictionary_UNK['UNK'] + 1
    return(dictionary_UNK, list(dictionary_UNK.keys()))
          
# Transform the data according to the dictionary_UNK
# Inputs : a splitted text, a dictionary from language_dictionary_UNK[0]
def splitted_text_UNK(splitted_text, dictionary_UNK, length):
    splitted_UNK = []
    for i in range(length):
        sentence = list(splitted_text[i])
        print(sentence)
        for j in range(len(sentence)):
            if sentence[j] not in dictionary_UNK.keys():
                sentence[j] = 'UNK'
        splitted_UNK.append(sentence)
    return(splitted_UNK)
    
def SOS_EOS(splitted_text,n):
    with_SOS_EOS = list(splitted_text)
    for i in range(len(splitted_text)):
        with_SOS_EOS[i] = ['SOS']*(n-1) + with_SOS_EOS[i] + ['EOS']*(n-1)
    return(with_SOS_EOS)


def group_words(L):
    out = L[0]
    for i in range(1,len(L)):
        out = out + " " + L[i]
    return(out)
    
#This function returns :
#the list of combinations of n-1 successive words in CURRENT
#for each combination of n-1 words of CURRENT, the list of possible next word in NEXT (making a n-gram)
#the associated probabilities in NEXT_PROBAS
def ngrams_list(splitted_text,n,length):
    new_text = SOS_EOS(splitted_text,n)
    CURRENT = []
    NEXT = []
    NEXT_PROBAS = []
    for i in range(length):
        sentence = new_text[i]
        for j in range(0,len(sentence)-(n-1)):
            current_word = group_words(sentence[j:j+n-1])
            next_word = sentence[j+n-1]
            if current_word in CURRENT:
                idx = CURRENT.index(current_word)
                if next_word in NEXT[idx]:
                    idx_next = NEXT[idx].index(next_word)
                    NEXT_PROBAS[idx][idx_next] = NEXT_PROBAS[idx][idx_next]+1
                else:
                    NEXT[idx].append(next_word)
                    NEXT_PROBAS[idx].append(1)
            else:
                CURRENT.append(current_word)
                NEXT.append([next_word])
                NEXT_PROBAS.append([1])
    return(CURRENT,NEXT,NEXT_PROBAS)  
#
#
#def laplace_smoothing(CURRENT, NEXT, NEXT_PROBAS, language_dictionnary_keys, smoothing_factor) :
#    CURRENT_LAP = list(CURRENT)
#    NEXT_LAP = list(NEXT)
#    NEXT_PROBAS_LAP = list(NEXT_PROBAS)
#    for c in range(len(CURRENT_LAP)):
#        for w in language_dictionnary_keys:
#            if w in NEXT_LAP[c]:
#                ind = NEXT_LAP[c].index(w)
#                NEXT_PROBAS_LAP[c][ind] += smoothing_factor
#            else:
#                NEXT_LAP[c].append(w)
#                NEXT_PROBAS_LAP[c].append(smoothing_factor)
#    return (CURRENT_LAP, NEXT_LAP, NEXT_PROBAS_LAP)
    
def laplace_smoothing(CURRENT, NEXT, NEXT_PROBAS, language_dictionnary_keys, smoothing_factor) :
    CURRENT_LAP = list([])
    NEXT_LAP = list([])
    NEXT_PROBAS_LAP = list([])
    for c in range(len(CURRENT)):
        CURRENT_LAP.append(CURRENT[c])
        NEXT_LAP.append(NEXT[c])
        NEXT_PROBAS_LAP.append(NEXT_PROBAS[c])
        for w in language_dictionnary_keys:
            if w in NEXT_LAP[c]:
                ind = NEXT_LAP[c].index(w)
                NEXT_PROBAS_LAP[c][ind] += smoothing_factor
            else:
                NEXT_LAP[c].append(w)
                NEXT_PROBAS_LAP[c].append(smoothing_factor)
    return (CURRENT_LAP, NEXT_LAP, NEXT_PROBAS_LAP)

def freq2proba(NEXT_PROBAS):
    OUTPUT = NEXT_PROBAS[:]
    for i in range(len(OUTPUT)):
        OUTPUT[i] = [x / sum(OUTPUT[i]) for x in OUTPUT[i]]
    return(OUTPUT) 


def naive_proba(input_string,CURRENT,NEXT,NEXT_PROBAS):
    proba = 1
    n = len(split_sentence(CURRENT[0])) + 1
    string = SOS_EOS(input_string,n)
    L = len(string[0])
    for i in range(L-n):
        print(i)
        substring = group_words(string[0][i:i+n-1])
        print(substring)
        lastword = string[0][i+n-1]
        if substring in CURRENT:
            idx = CURRENT.index(substring)
            if lastword in NEXT[idx]:
                idx_next = NEXT[idx].index(lastword)
                p = NEXT_PROBAS[idx][idx_next]
                print(p)
                proba = proba*p
            else:
                proba = 0
    return(proba)
                
