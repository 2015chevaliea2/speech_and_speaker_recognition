import numpy as np
from sklearn.mixture import log_multivariate_normal_density
from matplotlib.pyplot import pcolormesh
from proto2 import gmmloglik, forward

tidigits = np.load('lab2_tidigits.npz', encoding='bytes')['tidigits']
models = np.load('lab2_models.npz' , encoding='bytes')['models' ]
#print(models[3][b'hmm'].get(b'transmat'))
#print(models[0][b'hmm'].get(b'startprob'))
example = np.load( 'lab2_example.npz', encoding = 'bytes' )[ 'example' ].item()
#mfcc = tidigits[0].get(b'mfcc')
#pcolormesh(mfcc.T)


#==============================================================================
#  Question 4 after we have to change X by an utterance from tidigits
#==============================================================================
#X = example[b'mfcc']
#mu_gmm = models[0][b'gmm'].get(b'means')
#cv_gmm = models[0][b'gmm'].get(b'covars')
#mu_hmm = models[0][b'hmm'].get(b'means')
#cv_hmm = models[0][b'hmm'].get(b'covars')

#lpr_gmm = log_multivariate_normal_density(X,mu_gmm,cv_gmm,'diag')
#lpr_hmm = log_multivariate_normal_density(X,mu_hmm,cv_hmm,'diag')

#pcolormesh(X.T)
#pcolormesh(lpr_gmm.T)
#pcolormesh(lpr_hmm.T)

#==============================================================================
# question 5 
#==============================================================================
#
#example_gmmloglik = example[ b'gmm_loglik' ]
#weights = models[0][ b'gmm' ].get(b'weights')
#exp_gmmloglik = gmmloglik(lpr_gmm, weights)
#print(example_gmmloglik)
#print(exp_gmmloglik)

def compute_scores():
    scores = np.zeros((44,11))
    for i in range (44):
        for j in range (11):
            X = tidigits[i].get(b'mfcc')
            mu = models[j][b'gmm'].get(b'means')
            cv = models[j][b'gmm'].get(b'covars')
            weights = models[j][ b'gmm' ].get(b'weights')
            lpr_gmm = log_multivariate_normal_density(X,mu,cv,'diag')
            scores[i,j] = gmmloglik(lpr_gmm, weights)
    return (scores)

#scores = compute_scores
#print (compute_scores)
#winner_digit = np.argmax(scores, 1)
#print (winner_digit) #all the digits are well recognized

#==============================================================================
# question 6
#==============================================================================

X = example[b'mfcc']
mu = models[0][b'hmm'].get(b'means')
cv = models[0][b'hmm'].get(b'covars')
log_emlik = log_multivariate_normal_density(X,mu,cv,'diag')
log_startprob = np.log(models[0][b'hmm'].get(b'startprob'))
log_transmat =  np.log(models[0][b'hmm'].get(b'transmat'))

fwd = forward(log_emlik, log_startprob, log_transmat)

pcolormesh(fwd.T)



