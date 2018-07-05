from pylab import *
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

# Read a WAV file
# WAV file needs to be in same folder as the script
sampFreq, snd = wavfile.read('africa-test.wav')

# scipy.io.wavfile.read function reads wav files as int16 or int32 only
# Check data type using "snd.dtype"

# Convert sound array to floating point values ranging from -1 to 1
# Numerator value determines on data type of audio file
snd = snd / (2.**15)

# Shape returns sample points and number of channels
# print snd.shape

# Calculate time frame using the number of sample points divided by sampling rate
frameDuration = snd.shape[0]/sampFreq
print "Time duratione of audio: ", frameDuration, " seconds."

# Downsample in a kind of brutal way
snd_down = []
downFactor = 200
for i in range(len(snd)):
    if i % downFactor == 0:
        snd_down.append(snd[i])

print "Number of frames after downsampling: ", len(snd_down)

# List to array conversion
snd_down = np.asarray(snd_down)

# Perform amplitude envelope smoothing
# Calculate mean for desired number of frames
meanFrames = 10
# Initailize parameter
meanThreshold = 0
mTFactor = 1.5
for index in range(len(snd_down) - meanFrames):
    for idx in range(meanFrames - 1):
        meanThreshold = meanThreshold + abs(snd_down[index + idx])
    meanThreshold = meanThreshold / meanFrames

    if abs(snd_down[index]) > meanThreshold * mTFactor:
        snd_down[index] = 0

# Feature 1
# Time duration of clip that pass a given audio filter. Initial audio filter can be
# sound above a specific amplitude threshold. The frames that are higher than threshold
# are defined as HIGH, otherwise as LOW.

#plt.plot(snd_down)
#plt.ylabel('amplitude')
#plt.show()
fig, ax = plt.subplots()
# Plot duration of one minute
durationSeconds = 60
print "Duration examined: ", durationSeconds, "seconds"
ys = snd_down[:sampFreq/downFactor * durationSeconds]
threshold = 0.15
ax.axhline(y=threshold, color='r', linestyle=':')
ax.plot(ys)

# Count frames that are greater than threshold
greater_than_threshold = [i for i, val in enumerate(ys) if val>threshold]
# Calculate percentage
print "Percentage of high frames: ", float(len(greater_than_threshold))*100/len(ys), "%"

ax.plot(greater_than_threshold, ys[greater_than_threshold],
        linestyle='none', color='r', marker='o', markersize=3)
axes = plt.gca()
axes.set_ylim([-1,1])
plt.title("threshold set to %.2f" %threshold)
plt.show()

# Find max and min volume in clip
# print "max is ", snd.max
# print "min is ", snd.min

# Return Time duration of HIGH and LOW frames and also present in percentage

# Feature 2
# Option to ignore parts of the audio file. Starting from the beginning and the end for custom length

# Feature 3
# Custom audio filter design. This can be audio filter with sound above a specific amplitude over a certain period.
