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
# AmpFactor is for better visual presentaion
AmpFactor = 1.5

for index in range(len(snd_down) - meanFrames):
    for idx in range(meanFrames - 1):
        meanThreshold = meanThreshold + abs(snd_down[index + idx])
    meanThreshold = meanThreshold / meanFrames

    if abs(snd_down[index]) > meanThreshold * mTFactor:
        snd_down[index] = 0
    else:
        snd_down[index] = snd_down[index] * AmpFactor

# Feature 1
# Time duration of clip that pass a given audio filter. Initial audio filter can be
# sound above a specific amplitude threshold. The frames that are higher than threshold
# are defined as HIGH, otherwise as LOW.

# Plot duration of desired seconds
durationSeconds = 350
print "Duration examined: ", durationSeconds, "seconds"
ys = snd_down[:sampFreq/downFactor * durationSeconds]

# Due to processing below, frame index will not match the sampled time since
# a lot of unwanted frames will be discarded

# Remove a lot of very small non-zero values
for idx in range(len(ys)-1):
    if abs(ys[idx]) < 0.01:
        ys[idx] = 0
# Remove frames that are set to zero due to smoothing etc
ys = ys[ys != 0]

# --------------------------------------
# Calculate window statistics, window width is roughly 2s.
# If the percentage of frames in the window that are higher than threshold
# is over a limit, the window is assigned as HIGH, otherwise as LOW.
percentLimit = 0.5 # yet to be determined
windowSize = (sampFreq/downFactor) * 2
threshold = 0.06
# Use a for loop or a while loop here to shift the window through the audio.
# For each window position calculate the ratio(percent) of frames that are
# higher than threshold.
countArray = []
shiftIdx = 0
while ((shiftIdx+1)*windowSize) < len(ys):
    count = 0

    for i in range(shiftIdx*windowSize,(shiftIdx+1)*windowSize):

        if ys[i] > threshold:
            count = count + 1

    countArray.append(float(count)/windowSize)
    shiftIdx = shiftIdx + 1

# Used for debugging:
# print "performed ", shiftIdx, " shifts"
# print "should be close to ", float(len(ys))/windowSize

# Save all ratios of positions into an array.
# List to array conversion
countArray = np.asarray(countArray)
# Set a boundry value to group windows into HIGHs and LOWs.
boundryValue = 0.03
HIGH = 0
LOW = 0
for winIdx in range(len(countArray)):
    if countArray[winIdx] > boundryValue:
        HIGH = HIGH + 1
    else:
        LOW = LOW + 1
print "HIGH frame percentage is ", int(100*float(HIGH)/len(countArray)),"%"
print "LOW frame percentage is ", int(100*float(LOW)/len(countArray)),"%"
# --------------------------------------

f, (ax1, ax2) = plt.subplots(2, 1)

ax1.axhline(y=threshold, color='r', linestyle=':')
ax1.axhline(y=threshold*(-1), color='r', linestyle=':')
ax1.plot(ys)

ax2.axhline(y=boundryValue, color='r', linestyle=':')
ax2.plot(countArray)

ax1.set_ylim([-0.5,0.5])
ax2.set_ylim([0,0.5])
plt.suptitle("HIGH frame percentage: %i" %(int(100*float(HIGH)/len(countArray))))
plt.show()

# Feature 2
# Option to ignore parts of the audio file. Starting from the beginning and the end for custom length

# Feature 3
# Custom audio filter design. This can be audio filter with sound above a specific amplitude over a certain period.
