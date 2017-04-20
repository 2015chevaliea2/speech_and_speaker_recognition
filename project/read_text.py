import unicodedata
import string
import re
import random
from class_lang import Lang

# Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r"", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s

def readLangs(lang1, lang2, reverse=False):
    print("Reading lines...")

    # Read the file and split into lines
    lines = open('fra.txt', encoding = 'utf-8').read().strip().split('\n')
    
    # Split every line into pairs and normalize
    pairs = [[normalizeString(s) for s in l.split('\t')][0] for l in lines]
    pairs = list(set(pairs))
    # Reverse pairs, make Lang instances
    if reverse:
        pairs = [list(reversed(p)) for p in pairs]
        input_lang = Lang(lang2)
        output_lang = Lang(lang1)
    else:
        input_lang = Lang(lang1)
        output_lang = Lang(lang2)
        
    return input_lang, output_lang, pairs

def split_sentence(sentence):
    return(sentence.split(' '))

def split_txt():
    pairs = readLangs('ang', 'fra', reverse=False)[2]
    ans = []
    for i in range (len(pairs)):
        split = split_sentence(pairs[i])
        ans.append(split)
    return(ans)

#pairs = readLangs('ang', 'fra', reverse=False)[2]
#s = split_sentence(pairs[])
#splitted = split_txt()









