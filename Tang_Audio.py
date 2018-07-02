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

# Feature No.1
# Time duration of clip that has sound level over threshold

# Feature No.2
# 
