from functions import *
import pickle
splitted = split_txt() 
length = 100
#length = int(len(splitted)*0.8)
#input_string = list([["dock","day","to","be"]])

dico = language_dictionary(splitted,length) 
dico_UNK = language_dictionary_UNK(dico[0])   
splitted_UNK = splitted_text_UNK(splitted, dico_UNK[0], length) 

  #Definition of the ngram model 
c5,n5,p5 = ngrams_list(splitted_UNK,5,length)
proba5 = freq2proba(p5)
c4,n4,p4 = ngrams_list(splitted_UNK,4,length)
proba4 = freq2proba(p4)            
c3,n3,p3 = ngrams_list(splitted_UNK,3,length)
proba3 = freq2proba(p3)
c2,n2,p2 = ngrams_list(splitted_UNK,2,length)
proba2 = freq2proba(p2)
c1 = dico_UNK[1]
p1 = list(dico_UNK[0].values())
proba1 = [x / sum(p1) for x in p1]
n_grams = [[c1,[],proba1],[c2,n2,proba2],[c3,n3,proba3],[c4,n4,proba4],[c5,n5,proba5]]


with open('n_grams_model', 'wb') as fp:
    pickle.dump(n_grams, fp)

#Coefficients of the interpolation
#lambdas = np.array([1,1,1])/3
#                  
#sentence = "the price of gold is"
#string = preprocess(sentence,3,dico_UNK[0])
#result = interpolation(string,n_grams,lambdas)                  

#clap,nlap,n_plap = laplace_smoothing(c,n,n_p,dico_UNK[1],1)   
#n_p_proba = freq2proba(n_p) 
#p = naive_proba(input_string,clap,nlap,n_plap_proba)

#dictionary = language_dictionary(splitted2)[0]
#L = language_dictionary(splitted2)[1]
#M = bigrams(splitted2,L)

    
    
            
        










