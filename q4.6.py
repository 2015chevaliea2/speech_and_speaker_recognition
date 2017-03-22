from tools import *
from proto import *
from matplotlib.pyplot import imshow

tidigits = np.load( 'tidigits_python3.npz' )[ 'tidigits' ]



def mfcc(samples, winlen = 400, winshift = 200, nfft=512, nceps=13, samplingrate=20000, liftercoeff=22):
    """Computes Mel Frequency Cepstrum Coefficients.

    Args:
        samples: array of speech samples with shape (N,)
        winlen: lenght of the analysis window
        winshift: number of samples to shift the analysis window at every time step
        nfft: length of the Fast Fourier Transform (power of 2, >= winlen)
        nceps: number of cepstrum coefficients to compute
        samplingrate: sampling rate of the original signal
        liftercoeff: liftering coefficient used to equalise scale of MFCCs

    Returns:
        N x nceps array with lifetered MFCC coefficients
    """
    frames = enframe(samples, winlen, winshift)
    preemph = preemp(frames, 0.97)
    windowed = windowing(preemph)
    spec = powerSpectrum(windowed, nfft)
    mspec = logMelSpectrum(spec, samplingrate)
    ceps = cepstrum(mspec, nceps)
    return ([lifter(np.array(ceps), liftercoeff), mspec])


##compute mfccs    
mfccs = []
for i in range (len(tidigits)):
    mfcctd = mfcc(tidigits[i].get('samples'))
    mfccs.append(mfcctd)

#print (mfccs[0])   
#imshow(mfccs[33], aspect='auto', interpolation='nearest', origin='lower')
    
##concatenate mfcc in one feature
feature = []
for i in range (len(tidigits)):
    mfcci = mfcc(tidigits[i].get('samples'))[0]
    for k in range (len(mfcci)):
        feature.append(mfcci[k])

##concatenate mspec in one feature
# feature = []
# for i in range (len(tidigits)):
#     mspeci = mfcc(tidigits[i].get('samples'))[1]
#     for k in range (len(mspeci)):
#         feature.append(mspeci[k])

##Correlation coefficient

correlation_matrix = np.corrcoef(np.array(feature))

