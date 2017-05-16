from functions import *
import pickle
import numpy as np
#splitted = split_txt() 
#length = 100
length = int(len(splitted)*0.8)
#input_string = list([["dock","day","to","be"]])
#
#
#print('building dico')
#dico = language_dictionary(splitted,length) 
#print('building dico UNK')
#dico_UNK = language_dictionary_UNK(dico[0]) 
#print('processing splitted UNK')  
#splitted_UNK = splitted_text_UNK(splitted, dico_UNK[0], length) 
#
  #Definition of the ngram model 
s

#with open('n_grams_model', 'wb') as fp:
#    pickle.dump(n_grams, fp)

#Coefficients of the interpolation
<<<<<<< HEAD
lambdas = np.array([1,1,1,1,1])/5
#       
n = len(n_grams_model)           
sentence = "can you tell me where the toilets are"
string = preprocess(sentence, n, dico_UNK[0])
result1 = interpolation(string,n_grams_model,lambdas)                  
result2 = backoff(string, n, n_grams_model)
=======
#lambdas = np.array([1,1,1,1,1])/5
##       
#n = len(n_grams_model)           
#sentence = "the elephant is going in direction"
#string = preprocess(sentence, n, dico_UNK[0])
#result1 = interpolation(string,n_grams_model,lambdas)                  
#result2 = backoff(string, n, n_grams_model)
>>>>>>> 3ab2db0f1ca6c6857d6ae7b90a102f28b0fa93a2


#clap,nlap,n_plap = laplace_smoothing(c,n,n_p,dico_UNK[1],1)   
#n_p_proba = freq2proba(n_p) 
#p = naive_proba(input_string,clap,nlap,n_plap_proba)

#dictionary = language_dictionary(splitted2)[0]
#L = language_dictionary(splitted2)[1]
#M = bigrams(splitted2,L)

    
    
            
        










