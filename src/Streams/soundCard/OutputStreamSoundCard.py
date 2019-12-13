#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 22:43:41 2019

@author: nizar
"""
import sys
import sounddevice as sd #low level library for soundcard(hardware) use
sys.path.append('../../')
import Preconditions as p
from Streams.Stream import Stream
from Streams.Tracks import Track 
import numpy as np

class OutputStream_SoundCard(Stream):
    
    def __init__ (self, track, device=sd.default.device, launch=True):
        self.track = track
        self.stream = sd.OutputStream(samplerate=self.track.get_framerate(), device=device, channels=track.get_nchannels())
        super().__init__(None, False, launch)

        
    def open(self):
        self.stream.start()
        
    def write(self):
        self.stream.write(np.float32(self.track.data))
        
    def close(self):
        self.stream.stop()
        
        