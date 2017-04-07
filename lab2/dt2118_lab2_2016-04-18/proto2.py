import numpy as np
from tools2 import logsumexp

def gmmloglik(log_emlik, weights):
    """Log Likelihood for a GMM model based on Multivariate Normal Distribution.

    Args:
        log_emlik: array like, shape (N, K).
            contains the log likelihoods for each of N observations and
            each of K distributions
        weights:   weight vector for the K components in the mixture

    Output:
        gmmloglik: scalar, log likelihood of data given the GMM model.
    """
    N = len(log_emlik)
    ans = 0
    for j in range (N):
        arr = np.log(np.multiply(weights, np.exp(log_emlik[j])))
        ans = ans + logsumexp(arr, axis=0)
    return (ans)
    
def hmmloglik(logalpha):
    N = len(logalpha)
    return(logsumexp(logalpha[N-1,:]))

def forward(log_emlik, log_startprob, log_transmat):
    """Forward probabilities in log domain.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: log transition probability from state i to j

    Output:
        forward_prob: NxM array of forward log probabilities for each of the M states in the model
    """
    N = len(log_emlik)
    M = len(log_emlik[0])
    fwd_prob = np.zeros((N,M))
    for m in range (M):
        fwd_prob[0,m] = np.add(log_startprob[m],  log_emlik[0,m])
    for n in range (1,N):
        for m in range(M):
            arr = np.add(fwd_prob[n-1,:], log_transmat[:,m].T)
            lse = logsumexp(arr, axis=0)
            fwd_prob[n,m] = np.add(lse, log_emlik[n,m])
    return (fwd_prob)

def backward(log_emlik, log_startprob, log_transmat):
    """Backward probabilities in log domain.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: transition log probability from state i to j

    Output:
        backward_prob: NxM array of backward log probabilities for each of the M states in the model
    """

def viterbi(log_emlik, log_startprob, log_transmat):
    """Viterbi path.

    Args:
        log_emlik: NxM array of emission log likelihoods, N frames, M states
        log_startprob: log probability to start in state i
        log_transmat: transition log probability from state i to j

    Output:
        viterbi_loglik: log likelihood of the best path
        viterbi_path: best path
    """
