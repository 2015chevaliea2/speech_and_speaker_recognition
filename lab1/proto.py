# DT2118, Lab 1 Feature Extraction
from scipy.signal import lfilter
from scipy.signal import hamming
from scipy.fftpack import fft
from tools import trfbank
from scipy.fftpack.realtransforms import dct
from tools import *
import numpy as np

# Function given by the exercise ----------------------------------

def mfcc(samples, winlen = 400, winshift = 200, preempcoeff=0.97, nfft=512, nceps=13, samplingrate=20000, liftercoeff=22):
    """Computes Mel Frequency Cepstrum Coefficients.

    Args:
        samples: array of speech samples with shape (N,)
        winlen: lenght of the analysis window
        winshift: number of samples to shift the analysis window at every time step
        preempcoeff: pre-emphasis coefficient
        nfft: length of the Fast Fourier Transform (power of 2, >= winlen)
        nceps: number of cepstrum coefficients to compute
        samplingrate: sampling rate of the original signal
        liftercoeff: liftering coefficient used to equalise scale of MFCCs

    Returns:
        N x nceps array with lifetered MFCC coefficients
    """
    frames = enframe(samples, winlen, winshift)
    preemph = preemp(frames, preempcoeff)
    windowed = windowing(preemph)
    spec = powerSpectrum(windowed, nfft)
    mspec = logMelSpectrum(spec, samplingrate)
    ceps = cepstrum(mspec, nceps)
    return lifter(np.array(ceps), liftercoeff)

# Functions to be implemented ----------------------------------

def enframe(samples, winlen, winshift):
    """
    Slices the input samples into overlapping windows.

    Args:
        winlen: window length in samples.
        winshift: shift of consecutive windows in samples
    Returns:
        numpy array [N x winlen], where N is the number of windows that fit
        in the input signal
    """
    length = len(samples)
    sum = winlen
    ind = 0
    ans = []
    while sum<length-1:
        ans.append(samples[ind:ind+winlen])
        ind = sum - winshift
        sum = sum + winlen -winshift
    return(ans)
    
def preemp(input, p=0.97):
    """
    Pre-emphasis filter.

    Args:
        input: array of speech frames [N x M] where N is the number of frames and
               M the samples per frame
        p: preemhasis factor (defaults to the value specified in the exercise)

    Output:
        output: array of pre-emphasised speech samples
    Note (you can use the function lfilter from scipy.signal)
    """
    ans = []
    for i in range (len(input)):
        ans.append(lfilter([1,-p], [1], input[i], axis=-1, zi=None))
    return(ans)

def windowing(input):
    """
    Applies hamming window to the input frames.

    Args:
        input: array of speech samples [N x M] where N is the number of frames and
               M the samples per frame
    Output:
        array of windoed speech samples [N x M]
    Note (you can use the function hamming from scipy.signal, include the sym=0 option
    if you want to get the same results as in the example)
    """
    ans = []
    window = hamming(len(input[0]), sym=0 )
    for i in range (len(input)):
        ans.append(np.multiply(input[i], window))
    return(ans)

def powerSpectrum(input, nfft):
    """
    Calculates the power spectrum of the input signal, that is the square of the modulus of the FFT

    Args:
        input: array of speech samples [N x M] where N is the number of frames and
               M the samples per frame
        nfft: length of the FFT
    Output:
        array of power spectra [N x nfft]
    Note: you can use the function fft from scipy.fftpack
    """
    ans = []
    for i in range (len(input)):
        ans.append(np.square(np.absolute(fft(input[i], n=nfft, axis=-1, overwrite_x=False))))
    return(ans)

def logMelSpectrum(input, samplingrate):
    """
    Calculates the log output of a Mel filterbank when the input is the power spectrum

    Args:
        input: array of power spectrum coefficients [N x nfft] where N is the number of frames and
               nfft the length of each spectrum
        samplingrate: sampling rate of the original signal (used to calculate the filterbank shapes)
    Output:
        array of Mel filterbank log outputs [N x nmelfilters] where nmelfilters is the number
        of filters in the filterbank
    Note: use the trfbank function provided in tools.py to calculate the filterbank shapes and
          nmelfilters
    """
    fbank = trfbank(samplingrate, len(input[0]), lowfreq=133.33, linsc=200/3., logsc=1.0711703, nlinfilt=13, nlogfilt=27, equalareas=False)
    ans = np.dot(input, fbank.T)
    ans = np.log(ans)
    return(ans)

def cepstrum(input, nceps):
    """
    Calulates Cepstral coefficients from mel spectrum applying Discrete Cosine Transform

    Args:
        input: array of log outputs of Mel scale filterbank [N x nmelfilters] where N is the
               number of frames and nmelfilters the length of the filterbank
        nceps: number of output cepstral coefficients
    Output:
        array of Cepstral coefficients [N x nceps]
    Note: you can use the function dct from scipy.fftpack.realtransforms
    """
    ans = []
    for i in range (len(input)):
        ans.append((dct(input[i], type=2, n=None, axis=-1, norm='ortho', overwrite_x=False))[:nceps])
    res= []
    return(ans)
    

def dtw(x, y, dist):
    """Dynamic Time Warping.

    Args:
        x, y: arrays of size NxD and MxD respectively, where D is the dimensionality
              and N, M are the respective lenghts of the sequences
        dist: distance function (can be used in the code as dist(x[i], y[j]))

    Outputs:
        d: global distance between the sequences (scalar) normalized to len(x)+len(y)
        LD: local distance between frames from x and y (NxM matrix)
        AD: accumulated distance between frames of x and y (NxM matrix)
        path: best path thtough AD

    Note that you only need to define the first output for this exercise.
    """
    LD = dist(x,y)
    N = len(x)
    M = len(y)
    globaldist = np.zeros((N,M))
    antecedents = np.zeros((N,M,2))
    globaldist[0,0] = LD[0,0]
    for i in range(1,M):
        globaldist[0,i] = LD[0,i] + globaldist[0,i-1]
        antecedents[0,i] = [0,i-1]
    for i in range(1,N):
        globaldist[i,0] = LD[i,0] + globaldist[i-1,0]
        antecedents[i,0] = [i-1, 0]
    for n in range(1,N):
        for m in range(1,M):
            predecessors = [globaldist[n-1,m-1],globaldist[n,m-1],globaldist[n-1,m]]
            minimum = np.amin(predecessors)
            index = np.argmin(predecessors)
            globaldist[n,m] = LD[n,m]+ minimum
            if index == 0:
                antecedents[n,m] = [n-1,m-1]
            elif index == 1:
                antecedents[n,m] = [n,m-1]
            else :
                antecedents[n,m] = [n-1,m]
    AD = globaldist
    d = globaldist[N-1,M-1]/(N+M)
    
    abs, ord = [N-1,M-1]
    path = [[abs,ord]]
    while abs>0 and ord>0 :
        path.append(antecedents[abs,ord])
        abs , ord = antecedents[abs, ord]
    
    
    # while abs>0 or ord>0:
    #     if AD[abs-1,ord -1]<=AD[abs-1,ord] and AD[abs-1,ord-1]<=AD[abs,ord-1] and abs>0 and ord >0:
    #         path = path + [[abs-1,ord-1]]
    #         abs = abs-1
    #         ord = ord-1
    #     elif AD[abs,ord-1]<=AD[abs-1,ord-1] and AD[abs,ord-1]<=AD[abs-1,ord] and ord >0:
    #         path = path + [[abs,ord-1]]
    #         ord = ord-1
    #     elif abs>0:
    #         path = path + [[abs-1,ord]]
    #         abs = abs - 1
    
    # abs = 0
    # ord = 0
    # path = [[abs,ord]]
    # while abs<N-2 or ord<M-2:
    #     if AD[abs+1,ord +1]<=AD[abs+1,ord] and AD[abs+1,ord+1]<=AD[abs,ord+1] and abs<N-2 and ord<M-2:
    #         path = path + [[abs+1,ord+1]]
    #         abs = abs+1
    #         ord = ord+1
    #     elif AD[abs,ord+1]<=AD[abs+1,ord+1] and AD[abs,ord+1]<=AD[abs+1,ord] and ord<M-2:
    #         path = path + [[abs,ord+1]]
    #         ord = ord+1
    #     else:
    #         path = path + [[abs+1,ord]]
    #         abs = abs + 1

    return([d,LD,AD,path])

