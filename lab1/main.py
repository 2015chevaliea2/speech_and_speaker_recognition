import numpy as np
from proto import *
from matplotlib.pyplot import *
from scipy.io.wavfile import write
#import scikits.audiolab

example = np.load( 'example_python3.npz' )[ 'example' ].item()

sample = example.get('samples')
# write array to file:
#scikits.audiolab.wavwrite(sample, 'test.wav', len(sample), enc='pcm16')
## play the array:
#scikits.audiolab.play(sample, len(sample))

write('sample.wav', len(sample)+1, sample)


expframes = enframe(example.get('samples'),400,200)
print(example.get('frames')==np.array(expframes))
#imshow(example.get('frames'), aspect='auto', interpolation='nearest', origin='lower')
#imshow(expframes, aspect='auto', interpolation='nearest', origin='lower')

preempexp = preemp(expframes, p=0.97)
print(example.get('preemph')==np.array(preempexp))
#imshow(preempexp, aspect='auto', interpolation='nearest', origin='lower')

windowexp = windowing(preempexp)
print(example.get('windowed')==np.array(windowexp))
#imshow(example.get('windowed'), aspect='auto', interpolation='nearest', origin='lower')
#imshow(windowexp, aspect='auto', interpolation='nearest', origin='lower')

fftexp = powerSpectrum(windowexp, 512)
print(example.get('spec')-np.array(fftexp)<=0.00001)
#imshow(fftexp, aspect='auto', interpolation='nearest', origin='lower')
#imshow(np.array(fftexp), aspect='auto', interpolation='nearest', origin='lower')
#imshow(example.get('spec')-np.array(fftexp)<=0.00001, aspect='auto', interpolation='nearest', origin='lower')

mspecexp = logMelSpectrum(fftexp, 20000)
print(example.get('mspec')-np.array(mspecexp)<=0.00001)
#imshow(mspecexp, aspect='auto', interpolation='nearest', origin='lower')
#imshow(example.get('mspec'), aspect='auto', interpolation='nearest', origin='lower')

mfccexp = cepstrum(mspecexp, 13)
print(example.get('mfcc')-np.array(mfccexp)<=0.000001)
#imshow(lifter(np.array(mfccexp), 22), aspect='auto', interpolation='nearest', origin='lower')
#imshow(example.get('mfcc'), aspect='auto', interpolation='nearest', origin='lower')


