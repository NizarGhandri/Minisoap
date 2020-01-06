#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:08:04 2019

@author: nizar
"""
import sys
import sounddevice as sd #low level library for soundcard(hardware) use
sys.path.append('../../')
import Preconditions as p
from Streams.Stream import Stream
from Streams.Track import Track 

class InputStream_SoundCard (Stream):
    
    def __init__ (self, nchannels, framerate, samplewidth, device= sd.default.device, infinite= True, launch = True):
        self.framerate = framerate
        self.nchannels = nchannels
        self.samplewidth = samplewidth
        self.stream = sd.RawInputStream(samplerate=framerate, device = device, channels=nchannels, dtype="int"+str(8*samplewidth))
        super().__init__("None", infinite, launch)
        
        
    def open (self):
        self.launched = True
        self.stream.start()
        
    def close (self): 
        self.stream.stop()
        
    def read(self, n):
        p.check(n <= self.time() and self.launched)
        return Track(self.stream.read(n)[0], n, self.nchannels, self.samplewidth, self.framerate)
    
    def read_available(self, n):
        return Track(self.stream.read_available(n)[0], n, self.nchannels, self.samplewidth, self.framerate)
    
    def time (self):
        return self.stream.time
        
    def get_framerate(self):
        return self.framerate 
        
    def get_nchannels(self):
        return self.nchannels
        
        
        