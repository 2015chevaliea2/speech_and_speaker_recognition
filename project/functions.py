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
#        print(sentence)
        for j in range(len(sentence)):
            if sentence[j] not in dictionary_UNK.keys():
                sentence[j] = 'UNK'
        splitted_UNK.append(sentence)
    return(splitted_UNK)
    
# we add n-1 SOS tokens to compute the n-gram probabilities with interpolation and 1 EOS token
def SOS_EOS(splitted_text,n):
    with_SOS_EOS = list(splitted_text)
    for i in range(len(splitted_text)):
        with_SOS_EOS[i] = ['SOS']*(n-1) + with_SOS_EOS[i] 
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
        if i%1000 == 0:
            print(i)
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

# returns log2 probabilities
def freq2proba(NEXT_PROBAS):
    OUTPUT = NEXT_PROBAS[:]
    for i in range(len(OUTPUT)):
        OUTPUT[i] = np.log2(np.array([x / sum(OUTPUT[i]) for x in OUTPUT[i]]))
    return(OUTPUT) 


def naive_proba(input_string,CURRENT,NEXT,NEXT_PROBAS):
    proba = 0
    n = len(split_sentence(CURRENT[0])) + 1
    string = SOS_EOS(input_string,n)
    L = len(string[0])
    for i in range(L-n):
#        print(i)
        substring = group_words(string[0][i:i+n-1])
#        print(substring)
        lastword = string[0][i+n-1]
        if substring in CURRENT:
            idx = CURRENT.index(substring)
            if lastword in NEXT[idx]:
                idx_next = NEXT[idx].index(lastword)
                p = NEXT_PROBAS[idx][idx_next]
#                print(p)
                proba = proba + p
            else:
                proba = -np.inf
    return(proba)
                
def preprocess(sentence, n, dico_UNK):
    string = splitted_text_UNK([split_sentence(sentence)], dico_UNK, 1)
    string = SOS_EOS(string,n)
    return(string)

# Inputs : n_grams is a list whose lines contain the different models (1st line = [CURRENT,NEXT,NEXT_PROBAS] for n=1, etc)
# lambdas = vector of coefficients of the interpolation, in increasing order of ngrams, from unigram t ngram
# returns a log2 proba
def interpolation(string, n_grams, lambdas):
    lambdas = np.array(lambdas)
    n = len(lambdas)
#    print(string)
    size = len(string[0])
#    print(size)
    proba = 0
    for i in range(n-1,size):
#        print("i = ")
#        print(i)
        seq = string[0][i-n+1:i+1]
#        print(seq)
        p = np.zeros((n))
        for k in range(2, n+1):
#            print("k=")
#            print(k)
            substring = group_words(seq[n-k:n-1])
#            print(substring)
            lastword = seq[n-1]
            if substring in n_grams[k-1][0]:
                idx = n_grams[k-1][0].index(substring)
#                print("idx=")
#                print(idx)
                if lastword in n_grams[k-1][1][idx]:
                    idx_next = n_grams[k-1][1][idx].index(lastword)
                    p[k-1] = n_grams[k-1][2][idx][idx_next]
#                    print("yes!!")
                else:
                    p[k-1] = -np.inf
            else:
                p[k-1] = -np.inf
        idx = n_grams[0][0].index(lastword)
        p[0] = n_grams[0][2][idx]
        proba = proba + np.log2(np.dot(lambdas, np.power(2,p)))
    return(proba)
    
# returns a log2 proba
def backoff(string, n, n_grams):
    size = len(string[0])
    proba = 0
    tab = np.zeros((n))
    for i in range(n-1,size):
        seq = string[0][i-n+1:i+1]
#        print(seq)
        lastword = seq[n-1]
#        print(lastword)
        flag = True
        model = n
        while flag == True and model>1:
            substring = group_words(seq[0:len(seq)-1])
#            print(substring)
            if substring in n_grams[model-1][0]:
                idx = n_grams[model-1][0].index(substring)
                if lastword in n_grams[model-1][1][idx]:
                    idx_next = n_grams[model-1][1][idx].index(lastword)
                    p = n_grams[model-1][2][idx][idx_next]
                    proba = p + proba
#                    print("yes!!")
                    flag = False
#                    print(model)
                    tab[model-1] = tab[model-1]+1
                else:
                    model = model-1
                    seq = seq[1:len(seq)]
                    lastword = seq[len(seq)-1]
            else:
                model = model-1
                seq = seq[1:len(seq)]
                lastword = seq[len(seq)-1]
            
        if model == 1:
             idx = n_grams[0][0].index(lastword)
             p = n_grams[0][2][idx]
             proba = proba + p
             tab[model-1] = tab[model-1]+1
#             print(model)
    return(proba, tab)

#def perplexity(test_set, n, n_grams,dico_UNK):
#    len_set = len(test_set)
#    p_log_p = np.zeros((len_set))
#    for i in range(len_set):
#        merged_sentence = group_words(test_set[i])
#        string = preprocess(merged_sentence,n,dico_UNK[0])
#        p = backoff(string, n, n_grams)
##        print(p)
#        p_log_p[i] = p*np.power(2,p)
#        print(p_log_p[i])
#    entropy = - np.sum(p_log_p)
##    print(entropy)
#    perp = np.power(2,entropy)
#    return(perp)
    
def perplexity(test_set, n, n_grams,dico_UNK):
    len_set = len(test_set)
    CUR_test, NEXT_test, NEXT_FREQ_test = ngrams_list(test_set,n,len_set)
    NEXT_PROBAS_test = freq2proba(NEXT_FREQ_test)#These are log probabilities
    NEXT_PROBAS_test = np.power(2,NEXT_PROBAS_test)#Probas in non-log form
    LogQ = []
    for i in range(len(CUR_test)):
        LogQi = []
        for j in range(len(NEXT_test[i])):
            sentence = group_words([CUR_test[i],NEXT_test[i][j]])
            string = preprocess(sentence,n,dico_UNK[0])
            LogProba = backoff(string,n,n_grams)
            LogQi.append(LogProba)
        LogQ.append(LogQi)
    res = 0
    for i in range(len(NEXT_PROBAS_test)):
#        print(i)
        print(np.dot(NEXT_PROBAS_test[i],np.array(LogQ[i])))
        res = res + np.dot(NEXT_PROBAS_test[i],np.array(LogQ[i]))
    #-res is the entropy
    #2^(-res) is the perplexity
    return(np.power(2,-res))
        