from functions import *
splitted = split_txt() 
length = 100
#input_string = list([["dock","day","to","be"]])

dico = language_dictionary(splitted,length) 
dico_UNK = language_dictionary_UNK(dico[0])   
splitted_UNK = splitted_text_UNK(splitted, dico_UNK[0], length)                
c,n,n_p = ngrams_list(splitted,3,length)
#clap,nlap,n_plap = laplace_smoothing(c,n,n_p,dico_UNK[1],1)   
n_p_proba = freq2proba(n_p) 
#p = naive_proba(input_string,clap,nlap,n_plap_proba)

#dictionary = language_dictionary(splitted2)[0]
#L = language_dictionary(splitted2)[1]
#M = bigrams(splitted2,L)

    
    
            
        










