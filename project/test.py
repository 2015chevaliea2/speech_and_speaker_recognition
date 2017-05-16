from functions import *

#Coefficients of the interpolation
lambdas = np.array([1,1,1])/3
N = 5
sentence = "he pointed to the tower over there"
string = preprocess(sentence,N,dico_UNK[0])
#result_1 = interpolation(string,n_grams,lambdas)
result = backoff(string, N,n_grams_model)

test_set = splitted[74739:len(splitted)]
tab = np.zeros((N))
for i in range(len(test_set)):
    sentence = test_set[i]
    string = group_words(sentence)
    string = preprocess(string,N,dico_UNK[0])
    tab = tab + backoff(string,N,n_grams_model)[1]
    