import numpy as np
from scipy.signal import *
from scipy.fftpack import fft
from tools import trfbank
from matplotlib.pyplot import *

example = np.load( 'example_python3.npz' )[ 'example' ].item()

fbank = trfbank(20000, 512, lowfreq=133.33, linsc=200/3., logsc=1.0711703, nlinfilt=13, nlogfilt=27, equalareas=False)

imshow(fbank, aspect='auto', interpolation='nearest', origin='lower')

#imshow(example.get('mspec'), aspect='auto', interpolation='nearest', origin='lower')

window = hamming(400, sym=0 )
#plot(window)