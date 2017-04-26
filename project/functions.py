import unicodedata
import string
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
    
def SOS_EOS(splitted_text,n):
    with_SOS_EOS = list(splitted_text)
    for i in range(len(splitted_text)):
        with_SOS_EOS[i] = ['SOS']*n + with_SOS_EOS[i] + ['EOS']*n
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

#    NOT USEFUL ANYMORE, JUST A SPECIFIC CASE OF ngrams_list
def bigrams_list(splitted_text,length):
    CURRENT = []
    NEXT = []
    NEXT_PROBAS = []
    for i in range(length):
        sentence = splitted_text[i]
        for j in range(0,len(sentence)-1):
            current_word = sentence[j]
            next_word = sentence[j+1]
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

#    NOT USEFUL ANYMORE, JUST A SPECIFIC CASE OF ngrams_list
def trigrams_list(splitted_text,length):
    CURRENT = []
    NEXT = []
    NEXT_PROBAS = []
    for i in range(length):
        sentence = splitted_text[i]
        for j in range(0,len(sentence)-2):
            current_word = sentence[j]+" "+sentence[j+1]
            next_word = sentence[j+2]
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

def laplace_smoothing(CURRENT, NEXT, NEXT_PROBAS, language_dictionnary_keys, smoothing_factor) :
    CURRENT_LAP = CURRENT[:]
    NEXT_LAP = NEXT[:]
    NEXT_PROBAS_LAP = NEXT_PROBAS[:]
    for c in range(len(CURRENT_LAP)):
        for w in language_dictionnary_keys:
            if w in NEXT_LAP[c]:
                ind = NEXT_LAP[c].index(w)
                NEXT_PROBAS_LAP[c][ind] += smoothing_factor
            else:
                NEXT_LAP[c].append(w)
                NEXT_PROBAS_LAP[c].append(smoothing_factor)
    return (CURRENT_LAP, NEXT_LAP, NEXT_PROBAS_LAP)
    
#def back_off(input_string):
    