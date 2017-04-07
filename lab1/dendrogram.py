from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from tools import tidigit2labels
from scipy.spatial.distance import pdist

tidigits = np.load( 'tidigits_python3.npz' )[ 'tidigits' ]

M = np.loadtxt('44_ok')
link = linkage(pdist(M), method='complete')
label = tidigit2labels(tidigits)
dendro = dendrogram(link, labels = label, orientation='left')
show(dendro)