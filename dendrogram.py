from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from tools import tidigit2labels

tidigits = np.load( 'tidigits_python3.npz' )[ 'tidigits' ]

M = np.loadtxt('44x44M_bis')
link = linkage(M, method='complete')
label = tidigit2labels(tidigits)
dendro = dendrogram(link, labels = label, orientation='left')
show(dendro)