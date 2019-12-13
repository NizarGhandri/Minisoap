## @defgroup generators Generator module
# 
# This module should contain all track generators
# @{

import numpy as np
from Streams.Tracks import Track

## Generate sine wave by number of samples
#
#  @param A amplitude
#  @param n number of samples
#  @param f frequency
#  @param start second when to start
#  @param nchannels number of channels
#  @param samplewidth samplewidth
#  @param fs sampling frequency
#  @return sine wave track
def sine_n(A, n, f, start = 0, nchannels = 2, samplewidth = 2, fs=44100):
    frame_slice = np.arange(start, n)/fs
    samples = frame_slice
    for i in range(1,nchannels): 
        samples = np.column_stack((samples,frame_slice))
    signal = A*np.sin(2*np.pi*f*samples).reshape(n, nchannels)
    return Track(signal, n, nchannels, samplewidth, fs)
    

## Generate sine wave by seconds
#
#  @param A amplitude
#  @param t duration in seconds
#  @param f frequency
#  @param start second when to start
#  @param nchannels number of channels
#  @param samplewidth samplewidth
#  @param fs sampling frequency
#  @return sine wave track
def sine_t(A, t, f, start = 0, nchannels = 2, samplewidth = 2, fs=44100):
    return sine_n(A, t*fs, f, start = start*fs, nchannels = nchannels, samplewidth = samplewidth, fs= fs)
    
    
## Generate constant wave by number of samples
#
#  @param n number of samples
#  @param value value of wave
#  @param start second when to start
#  @param nchannels number of channels
#  @param samplewidth samplewidth
#  @param fs sampling frequency
#  @return constant track
def constant_n(n, value, start = 0, nchannels = 2, samplewidth=2, fs=44100):
    frame_slice = np.arange(start, n)/fs
    samples = frame_slice
    for i in range(1,nchannels): 
        samples = np.column_stack((samples,frame_slice))
    signal = 0*samples + value
    signal.reshape(n, nchannels)
    return Track(signal, n, nchannels, samplewidth, fs)


## Generate constant wave by seconds
#
#  @param t number of seconds
#  @param value value of wave
#  @param start second when to start
#  @param nchannels number of channels
#  @param samplewidth samplewidth
#  @param fs sampling frequency
#  @return constant track
def constant_t(t, value, start = 0, nchannels = 2, samplewidth = 2, fs=44100):
    return constant_n(t*fs, value, start = start*fs, nchannels = nchannels, samplewidth = samplewidth, fs= fs)
    
    


# @}




