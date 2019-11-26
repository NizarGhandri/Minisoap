#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 23:47:04 2019

@author: nizar
"""
import numpy as np
import Preconditions as p

class Track ():
    
    def __init__ (self, data, nframes, nchannels, samplewidth=2, framerate= 44100):
        self.size = nframes
        self.nchannels = nchannels
        self.samplewidth = samplewidth
        self.framerate = framerate
        if(type(data) == bytes):
            p.check(nframes*samplewidth*nchannels == len(data))
            self.data = self.byte_float_converter(data)
        else: 
            p.check(data.shape == (nframes, nchannels))
            self.data = np.array(data)
            
        
    def get_nchannels(self):
        return self.nchannels
    
    def get_raw_data(self):
        return self.float_byte_converter(self.data)
    
    def get_data(self):
        return np.array(self.data)
    
    def get_size(self):
        return self.size 
    
    def get_samplewidth(self):
        return self.samplewidth
    
    def get_framerate(self):
        return self.framerate 
    
    def get_time(self):
        return self.framerate*self.size
    
    def byte_float_converter (self, data): #can't use struct.unpack because of the 24 bit format.
        step = self.nchannels
        size = self.size
        samp = self.samplewidth
        returned = np.zeros((size,step))
        for i in range(size):
            for k in range(step):
                start = i*samp*step+k*samp
                end = start+ samp
                returned [i, k] = int.from_bytes(data[start:end], "big")
        return returned/2**(8*samp-1) - 1
    
    def float_byte_converter (self, array): 
        samp = self.samplewidth
        interm = (array+1) * 2**(8*samp-1)
        returned = bytes()
        for i in range(self.size):
            for k in range(self.nchannels):
                returned += int.to_bytes(int(interm[i, k]), samp, 'big') 
        return returned
    
    def get_data_slice (self, start_time, end_time):
        return np.array(self.data[int(self.framerate*start_time):int(self.framerate*end_time)])
                          
                        
    def extend_with_zeroes_front (self, n):
        return np.concatenate((np.zeros((n, self.nchannels)), np.array(self.data)))
    
    def extend_with_zeroes_behind (self, n): 
        return np.concatenate((np.array(self.data), np.zeros((n, self.nchannels))))
                    
                    

    
    
        