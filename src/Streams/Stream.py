#!/usr/bin/env python
# coding: utf-8

# # Stream class
# 
# This class is a wrapper of the wave library that will allow us to make better use of it and adapt it to our project architecture.
# 
# For now it is very elementary but it will be upgraded slowly according to our needs and how the project evolves. 
# 
# TODO: 
# 
# -> finish write method and other utilitary methods. 
# 
# -> read and write are blocking methods so one can use an asynchronous manner of coding and add a callback for efficiency. 
# 
# -> define a better data structre for the return type of read
# 
# -> add compression: we can add a compression feature to the stream one we output the data. (encoding and decoding of course) 
# 
# -> fix constants
# 
# -> storing signals does not necessarly require space one could you the fast discrete fourrier transform and store only a function/lambda (idea to ponder)s.

# Include necessary imports here.




import wave
from src.Preconditions import Preconditions as p
from abc import ABC, abstractmethod
 


# 
# Here we define stream class constructor and add the open and close methods. 
# we specify if a stream is infinite or not, if it should be started/opened directly or not and its type (input or output). There additional parameters which were set to satisfy standard CD quality, these parameters should only be modified if we are outputing a stream.




class Stream(ABC): 
    
    def __init__ (self, file, infinite = False, launch = True): #nchannels=2, sampwidth=2, framerate=44100, nframes=1024):
        self.file = file
        self.infinite = infinite
        #self.input_signal = self.input_signal
        #self.output_signal = output_signal
        #if(output_signal): 
        #    self.wave_parameters = (nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed')
        #p.check(not(input_signal and output_signal),
        #        "the stream must be either an output stream or an input stream")
        if (launch):
            self.open()
            
    @abstractmethod      
    def open(self, mode):
        p.check(self.launched, "cannot open already launched stream")
        #p.check(mode, lambda x: x == 'rb' or x == 'wb', "specify correct mode to open" )
        try:
            self.wave_signal = wave.open(self.file, mode)  #getting rid of expensive try catch 
            self.launched = True
            
        except: 
            p.eprint("IOError occured while opening file %s in %s mode", self.file, mode)
            
    @abstractmethod        
    def close(self): 
        p.check(not(self.launched), "cannot close unopened stream")
        self.wave_signal.close()
        
    
            

