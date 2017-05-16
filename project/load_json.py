from functions import *
import numpy as np
import itertools
import json
json_file = open('this_medicine_helps_relieve_muscle_pain')
json_str = json_file.read()
json_data = json.loads(json_str)
j = json_data.get('results')[0]['word_alternatives']
n_words = len(j)

N = 1

list_word = []
list_word_confidence = []
for i in range(n_words):
    alternatives = j[i].get('alternatives')
    list_wordi = []
    list_wordprobai = []
    for k in range(len(alternatives)):
        word = alternatives[k].get('word')
        confidence = alternatives[k].get('confidence')
        list_wordi.append(word)
        list_wordprobai.append(confidence)
    list_word.append(list_wordi)
    list_word_confidence.append(list_wordprobai)
    
hypotheses = []
hypotheses_proba = []
for i in itertools.product(*list_word):
    hypotheses.append(i)
#    print(i)
for i in itertools.product(*list_word_confidence):
    hypotheses_proba.append(i)
hypotheses_proba = np.prod(hypotheses_proba,axis = 1)

our_proba = np.zeros(len(hypotheses))
for i in range(len(hypotheses)):
    string = group_words(hypotheses[i])
    string = normalizeString(string)
    hypotheses[i] = string
    string = preprocess(string,N,dico_UNK[0])
    our_proba[i] = backoff(string,N,n_grams_model)
our_proba = np.power(2,our_proba)#from log probas to probas
    
#sort list
sorted_ngram1= [h for (x,h) in sorted(zip(our_proba,hypotheses))]
sorted_watson= [h for (x,h) in sorted(zip(hypotheses_proba,hypotheses))]
