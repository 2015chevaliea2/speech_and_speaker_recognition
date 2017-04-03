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


## No test set
# utterance = []
# digit = '7'
# for i in range(len(tidigits)):
#     if tidigits[i].get('digit') == digit:
#         utterancei=(mfcc(tidigits[i].get('samples')))
#         for k in range (len(utterancei)):
#             utterance.append(utterancei[k])

G.fit(mfcc(tidigits[16].get('samples')))
plot(G.means_)

# a = np.zeros((1,13))
# b= G.predict(a)
# G.predict([[1,2,3,2,4,2,5,6,7,4,5,6,3]])


# M = np.zeros((nb,nb))
# M = dist(G.means_ , G.means_)

# for i in range(nb):
#     for j in range(nb):
#         x = np.array(G.means_[i,:])
#         y = np.array(G.means_[j,:])
#         M[i,j] = dist(x,y)
        
#pcolormesh(M)

# link = linkage(M, method='complete')
# dendro = dendrogram(link, orientation='left')
# show(dendro)