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
from Streams.Track import Track 

class OutputStream_SoundCard(Stream):
    
    
    def __init__ (self, track, device=sd.default.device, launch=True):
        self.track = track
        self.device = device
        self.stream = sd.RawOutputStream(samplerate=self.track.get_framerate(), device=self.device, channels=track.get_nchannels(), dtype="int"+str(track.get_samplewidth()*8))        
        super().__init__("None", False, launch)
        
    def open(self):
        self.stream.start()
        
    def write(self): 
        self.stream.write(self.track.get_raw_data())
        
    def close(self):
        self.stream.stop()
        
        