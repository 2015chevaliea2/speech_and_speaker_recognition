from functions import *
import pickle
#splitted = split_txt() 
#length = 100
#length = int(len(splitted)*0.8)
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
#  #Definition of the ngram model 
#print('5-gram')
#c5,n5,p5 = ngrams_list(splitted_UNK,5,length)
#print('5-gram proba')
#proba5 = freq2proba(p5)
#print('4-gram')
#c4,n4,p4 = ngrams_list(splitted_UNK,4,length)
#print('4-gram proba')
#proba4 = freq2proba(p4)  
#print('3-gram')          
#c3,n3,p3 = ngrams_list(splitted_UNK,3,length)
#print('3-gram proba')
#proba3 = freq2proba(p3)
#print('2-gram')
#c2,n2,p2 = ngrams_list(splitted_UNK,2,length)
#print('2-gram proba')
#proba2 = freq2proba(p2)
#print('1-gram')
#c1 = dico_UNK[1]
#p1 = list(dico_UNK[0].values())
#print('1-gram proba')
#proba1 = [x / sum(p1) for x in p1]
#n_grams = [[c1,[],proba1],[c2,n2,proba2],[c3,n3,proba3],[c4,n4,proba4],[c5,n5,proba5]]
#
#
#with open('n_grams_model', 'wb') as fp:
#    pickle.dump(n_grams, fp)

#Coefficients of the interpolation
lambdas = np.array([1,1,1,1,1])/5
#       
n = len(n_grams_model)           
sentence = "the elephant is going in direction"
string = preprocess(sentence, n, dico_UNK[0])
result1 = interpolation(string,n_grams_model,lambdas)                  
result2 = backoff(string, n, n_grams_model)


#clap,nlap,n_plap = laplace_smoothing(c,n,n_p,dico_UNK[1],1)   
#n_p_proba = freq2proba(n_p) 
#p = naive_proba(input_string,clap,nlap,n_plap_proba)

#dictionary = language_dictionary(splitted2)[0]
#L = language_dictionary(splitted2)[1]
#M = bigrams(splitted2,L)

    
    
            
        










