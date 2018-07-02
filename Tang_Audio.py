from pylab import *
from scipy.io import wavfile

# read in a wav file
sampFreq, snd = wavfile.read('440_sine.wav')

# scipy.io.wavfile.read function reads wav files as int16 or int32 only
# check using "snd.dtype"

# convert sound array to floating point values ranging from -1 to 1
snd = snd / (2.**15)
# shape shows number of channels and sample points
# snd.shape

# Calculate time frame using the number of sample points divided by sampling rate

# Feature 1
# Time duration of clip that pass a given audio filter. Initial audio filter can be 
# sound above a specific amplitude threshold 

# Feature 2
# Option to ignore parts of the audio file. Starting from the beginning and the end for custom length

# Feature 3
# Custom audio filter design. This can be audio filter with sound above a specific amplitude over a certain period.

