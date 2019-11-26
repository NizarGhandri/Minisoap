## @defgroup operations Operations module
# 
# This module should contain all operations available on tracks
# @{

from Streams.Tracks import Track
import numpy as np
import Preconditions as p

## Nullify a track
#
#  @param track the track
#  @param start second when to start
#  @param end second when to end
#  @return new modified track
def nullify(track, start=0, end=None):
    if (end is None):
        return amplitude(track, 0)
    else:
        return Track(np.concatenate((track.get_data_slice(0, start), track.get_data_slice(start, end)*0, track.get_data_slice(end, track.get_time()))), track.get_size(), track.get_nchannels(), track.get_samplewidth(), track.get_framerate())


## Multiply amplitude of track
#
#  @param track the track
#  @param a amplitude multiplication factor
#  @return new modified track
def amplitude(track, a):
    return Track(a*track.get_data(), track.get_size(), track.get_nchannels(), track.get_samplewidth(), track.get_framerate())

## Convolve two tracks
#
#  @param track first track
#  @param track2 second track
#  @return new modified track
def convolve(track, track2):
    p.check_same_params(track, track2)
    return Track(np.convolve(track.get_data(), track2.get_data()), track.get_size(), track.get_nchannels(), track.get_samplewidth(), track.get_framerate())


## Mix two tracks
#
#  @param track first track
#  @param track2 second track
#  @param a1 amplitude multiplier of frist track
#  @param a2 amplitude multiplier of second track
#  @return new modified track
def add(track, track2, t, a1=0.5, a2=0.5):
    p.check_same_params(track, track2)
    r = t*track2.get_framerate()
    extention_frames_b = track2.get_size() - r
    extention_frames_f = track.get_size() - r
    return Track(a1*track.extend_with_zeroes_behind(extention_frames_b) + a2*track2.extend_with_zeroes_front(extention_frames_f), extention_frames_b + extention_frames_f + r, track.get_nchannels(), track.get_samplewidth(), track.get_framerate())


## Join two tracks in stereo
#
#  @param track first track
#  @param track2 second track
#  @return new modified track
def mono_to_stereo(track, track2):
    p.check(track.get_nchannels() == 1 and track2.get_nchannels() == 1, details ="non mono Tracks")
    p.check_same_params(track, track2)
    return Track(np.column_stack((track.get_data(), track2.get_data())), track.get_size(), 2, track.get_samplewidth(), track.get_framerate())


## Fade a track
#
#  @param track first track
#  @param factor fading factor
#  @param t second when to start the fade
#  @return new modified track
def fade_exp(track, factor, t):
    d = track.get_data_slice(t, track.get_size()/track.get_framerate())
    return Track(np.concatenate((track.get_data_slice(0, t), np.array([d[k, ]*2**(-factor*(k)) for k in range(np.shape(d)[0])]))), track.get_size(), track.get_nchannels(), track.get_samplewidth(), track.get_framerate()) 


## Fade inverse a track
#
#  @param track first track
#  @param factor fading factor
#  @param t second when to start the fade
#  @return new modified track
def fade_inv(track, factor, t):
    d = track.get_data_slice(0, t)
    return Track(np.concatenate((d * np.array([d[k, ]*(1-2**(-factor*(k))) for k in range(np.shape(d)[0])]), track.get_data_slice(t, track.get_size()/track.get_framerate()))), track.get_size(), track.get_nchannels(), track.get_samplewidth(), track.get_framerate()) 


## Crossfade two track
#
#  @param track1 first track
#  @param track2 second track
#  @param factor fading factor
#  @param t second when to start the fade
#  @return new modified track
def crossfade_exp(track1, track2, factor, t):
    p.check_same_params(track1, track2)
    return add(fade_exp(track1, factor), fade_inv(track2, factor), t, a1=1, a2 =1)



#@}
