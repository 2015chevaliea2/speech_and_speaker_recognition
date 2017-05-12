import pickle

with open ('n_grams_model', 'rb') as fp:
    n_grams_model = pickle.load(fp)

with open ('splitted', 'rb') as fp:
    splitted = pickle.load(fp)
    
with open ('splitted_UNK', 'rb') as fp:
    splitted_UNK = pickle.load(fp)
    
with open ('dico', 'rb') as fp:
    dico = pickle.load(fp)
    
with open ('dico_UNK', 'rb') as fp:
    dico_UNK = pickle.load(fp)