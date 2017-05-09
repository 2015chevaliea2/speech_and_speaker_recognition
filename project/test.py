from functions import *

#Coefficients of the interpolation
lambdas = np.array([1,1,1])/3

sentence = "the price of gold"
string = preprocess(sentence,3,dico_UNK[0])
#result = interpolation(string,n_grams,lambdas)
result = backup(string, n_grams)