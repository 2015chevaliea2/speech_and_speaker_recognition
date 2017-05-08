# -*- coding: utf-8 -*-
"""
Created on Mon May  8 13:12:47 2017

@author: Arnaud
"""

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

def bigrams(splitted_text,L):
    N = len(dictionary)
    transition_mat = np.zeros((N,N))
    for i in range(L):
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
