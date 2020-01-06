#!/usr/bin/env python
# coding: utf-8




## Stream class
# 
# This class is a mother class of all streams in the project.

import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/..')

import wave
import Preconditions as p
from abc import ABC, abstractmethod






class Stream(ABC): 
    
    file_extention_index = -3
    supported_file_extention = "wav"
    
    ## constructor
    # @params: defines the source or destination of the stream can be a soundcard or a file ... 
    # @params: defines if the stream can be infinite or not it is set by default to False (for local files)
    # @params: decides if we open directly the stream or we wait for the user to call the open method, it is set by default to True
    def __init__ (self, file, infinite = False, launch = True): #nchannels=2, sampwidth=2, framerate=44100, nframes=1024):
        self.infinite = infinite
        self.launched = launch
        self.wave_signal = None
        
        self.file = file
        self.file_format = file[self.file_extention_index:]
        self.file = file[:self.file_extention_index] + self.supported_file_extention
        
        if (launch):
            self.open()
    ##open
    # @params: mode defines the way we are opening the stream (reading or wirtting)
    # 
    #opens the stream        
    @abstractmethod      
    def open(self, mode):
        p.check(self.launched, details = "cannot open already launched stream")
        try:
            
            self.wave_signal = wave.open(self.file, mode)  
            self.launched = True
            
            
        except: 
            p.eprint("IOError occured while opening file {!r} in {!r} mode".format(self.file, mode))
    ##close
    # 
    # closes the stream         
    @abstractmethod        
    def close(self): 
        p.check(self.launched, details ="cannot close unopened stream")
        self.wave_signal.close()
                
                
    
