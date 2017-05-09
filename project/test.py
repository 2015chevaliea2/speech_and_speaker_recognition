from functions import *

sentence = "gold is fresh"
string = preprocess(sentence,3,dico_UNK[0])
result = interpolation(string,n_grams,lambdas)
