from sklearn import mixture
import numpy as np
from proto import mfcc
from tools import dist
from matplotlib.pyplot import *
from scipy.cluster.hierarchy import dendrogram, linkage

nb=32
G = mixture.GMM(nb)

tidigits = np.load( 'tidigits_python3.npz' )[ 'tidigits' ]



## test set nd training set for utterances
# train_utterance = []
# test_utterance = []
# digit = '7'
# count = 0
# for i in range(len(tidigits)):
#     if tidigits[i].get('digit') == digit and count < 3:
#         count = count +1
#         utterancei=(mfcc(tidigits[i].get('samples')))
#         for k in range (len(utterancei)):
#             train_utterance.append(utterancei[k])
#     elif tidigits[i].get('digit') == digit and count==3:
#         utterancei=(mfcc(tidigits[i].get('samples')))
#         for k in range (len(utterancei)):
#             test_utterance.append(utterancei[k])

# G.fit(train_utterance)
# proba = G.predict(test_utterance)
# print(proba)


## train GMM on all data
utterance = []

for i in range(len(tidigits)):
    utterancei=(mfcc(tidigits[i].get('samples')))
    for k in range (len(utterancei)):
        utterance.append(utterancei[k])

G.fit(utterance)

c16 = G.predict(mfcc(tidigits[16].get('samples')))
c17 = G.predict(mfcc(tidigits[17].get('samples')))
c38 = G.predict(mfcc(tidigits[38].get('samples')))
c39 = G.predict(mfcc(tidigits[39].get('samples')))

figure(1)
subplot(221)
plot(c16, 'r^')
title('man, 16')
subplot(222)
plot(c17, 'rs')
title('man, 17')
subplot(223)
plot(c38, 'g^')
title('woman, 38')
subplot(224)
plot(c39, 'gs')
title('woman, 39') 
show()