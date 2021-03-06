import numpy as np
from sklearn.mixture import log_multivariate_normal_density
from matplotlib.pyplot import pcolormesh, imshow, plot
from proto2 import gmmloglik, forward, hmmloglik, viterbi,backward

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

#sore the utterances
def compute_scores_gmm():
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
#
#scores_gmm = compute_scores_gmm()
#print (scores_gmm)
#winner_digit_gmm = np.argmax(scores_gmm, 1)
#print (winner_digit_gmm) #all the digits are well recognized

#==============================================================================
# question 6 
#==============================================================================

#the code is OK there is just a problemn comparing -inf and -inf
#X = example[b'mfcc']
#mu = models[0][b'hmm'].get(b'means')
#cv = models[0][b'hmm'].get(b'covars')
#log_emlik = log_multivariate_normal_density(X,mu,cv,'diag')
#log_startprob = np.log(models[0][b'hmm'].get(b'startprob'))
#log_transmat =  np.log(models[0][b'hmm'].get(b'transmat'))
#
#fwd = forward(log_emlik, log_startprob, log_transmat)
#example_logalpha = example[ b'hmm_logalpha' ]
#pcolormesh (abs(fwd-example_logalpha).T<0.0001)
#print(example_logalpha)
#print(fwd)
#imshow(example_logalpha.T ,origin= 'lower' ,interpolation= 'nearest' ,aspect= 'auto')

#to plot the latice alpha
#there is a problem plotting
#imshow(np.exp(fwd).T ,origin= 'lower' ,interpolation= 'nearest' ,aspect= 'auto')


#the two hmm_loglik are equals
#exp_hmmloglik = hmmloglik(fwd)
#print (example[ b'hmm_loglik' ])
#print (exp_hmmloglik)

#compute all hmm_scores

def compute_scores_hmm():
    scores = np.zeros((44,11))
    for i in range (44):
        for j in range (11):
            X = tidigits[i].get(b'mfcc')
            mu = models[j][b'hmm'].get(b'means')
            cv = models[j][b'hmm'].get(b'covars')
            log_emlik = log_multivariate_normal_density(X,mu,cv,'diag')
            log_startprob = np.log(models[j][b'hmm'].get(b'startprob'))
            log_transmat =  np.log(models[j][b'hmm'].get(b'transmat'))
            fwd = forward(log_emlik, log_startprob, log_transmat)
            scores[i,j] = hmmloglik(fwd)
    return (scores)

#scores_hmm = compute_scores_hmm()
#print (scores_hmm)
#winner_digit_hmm = np.argmax(scores_hmm, 1)
#print (winner_digit_hmm) #some digits are miss classified
            
def compute_scores_hmm2gmm():
    scores = np.zeros((44,11))
    for i in range (44):
        for j in range (11):
            X = tidigits[i].get(b'mfcc')
            mu = models[j][b'hmm'].get(b'means')
            cv = models[j][b'hmm'].get(b'covars')
            weights = 1/len(mu)*np.ones(len(mu))
            lpr_hmm = log_multivariate_normal_density(X,mu,cv,'diag')
            scores[i,j] = gmmloglik(lpr_hmm, weights)
    return(scores)

scores_hmm2gmm = compute_scores_hmm2gmm()
print (scores_hmm2gmm)
winner_digit_hmm2gmm = np.argmax(scores_hmm2gmm, 1)
print (winner_digit_hmm2gmm) #all th digits are well recognized

#==============================================================================
# Question 7 Viterbi is OK
#==============================================================================

#X = tidigits[16][b'mfcc']
#mu = models[8][b'hmm'].get(b'means')
#cv = models[8][b'hmm'].get(b'covars')
#log_emlik = log_multivariate_normal_density(X,mu,cv,'diag')
#log_startprob = np.log(models[8][b'hmm'].get(b'startprob'))
#log_transmat =  np.log(models[8][b'hmm'].get(b'transmat'))
#
#expv = viterbi(log_emlik, log_startprob, log_transmat)
#example_vloglik= example[b'hmm_vloglik']
#imshow(expv[0].T ,origin= 'lower' ,interpolation= 'nearest' ,aspect= 'auto')
#plot(np.flipud(expv[1]))

#compute viterbi loglik and check equality with example
#exp_vloglik = hmmloglik(expv[0])
#print (exp_vloglik, np.flipud(expv[1]))
#print (example_vloglik)
#print (np.flipud(expv[1]))
#print (abs(exp_vloglik-example_vloglik[0])<0.00001)
#print (abs(np.flipud(expv[1]) - example_vloglik[1])<0.00001)

def compute_scores_viterbi():
    scores = np.zeros((44,11))
    for i in range (44):
        for j in range (11):
            X = tidigits[i].get(b'mfcc')
            mu = models[j][b'hmm'].get(b'means')
            cv = models[j][b'hmm'].get(b'covars')
            log_emlik = log_multivariate_normal_density(X,mu,cv,'diag')
            log_startprob = np.log(models[j][b'hmm'].get(b'startprob'))
            log_transmat =  np.log(models[j][b'hmm'].get(b'transmat'))
            vit = viterbi(log_emlik, log_startprob, log_transmat)
            scores[i,j] = hmmloglik(vit[0])
    return(scores)

#scores_viterbi = compute_scores_viterbi()
#print (scores_viterbi)
#winner_digit_viterbi = np.argmax(scores_viterbi, 1)
#print (winner_digit_viterbi) #some utterances are missclssified we count 2 mistakes

#==============================================================================
# Optional : backward
#==============================================================================
#X = example[b'mfcc']
#mu = models[0][b'hmm'].get(b'means')
#cv = models[0][b'hmm'].get(b'covars')
#log_emlik = log_multivariate_normal_density(X,mu,cv,'diag')
#log_startprob = np.log(models[0][b'hmm'].get(b'startprob'))
#log_transmat =  np.log(models[0][b'hmm'].get(b'transmat'))
#bwd = backward(log_emlik, log_startprob, log_transmat)
#example_logbeta = example[ b'hmm_logbeta' ]
#pcolormesh (abs(bwd-example_logbeta).T<0.0001)

#We obtain the same results as the example
