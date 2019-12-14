#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 23:47:04 2019

@author: nizar
"""
import sys
sys.path.append("../../")
import numpy as np
import src.Preconditions as p


## Track
#this class is the lowest level of encapsulation of the data of the audio, this class is designed to be "immutable" so we can keep the old data as well.
#this is the data type used by the operations the generators and the output streams


 
class Track ():
    
    ##constructor 
    # @params: data in bytes or ints
    # @params: wave parameters to add 
    def __init__ (self, data, nframes, nchannels, samplewidth=2, framerate= 44100):
        self.size = nframes
        self.nchannels = nchannels
        self.samplewidth = samplewidth
        self.framerate = framerate
        self.time = framerate * nframes 
        if(type(data) == bytes):
            p.check(nframes*samplewidth*nchannels == len(data))
            self.data = self.byte_float_converter(data)
        else: 
            p.check(data.shape == (nframes, nchannels))
            self.data = np.array(data)
            
    ####### getters of the attributes 
    
    
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
    ## get_time
    # returns how long in seconds the Track is 
    def get_time(self):
        return self.time
    ## byte_float_converter: 
    # @params: data in bytes
    # method to convert the bytearray returned by reading the wav file into an array of normalized floating point numbers (-1, 1)
    def byte_float_converter (self, data): #can't use struct.unpack because of the 24 bit format.
        step = self.nchannels
        size = self.size
        samp = self.samplewidth
        returned = np.zeros((size,step))
        for i in range(size):
            for k in range(step):
                start = i*samp*step+k*samp
                end = start+ samp
                returned [i, k] = int.from_bytes(data[start:end], "little")
        return returned
    ## float_byte_converter
    # @params: data in floating point
    # method to convert back the floating point array with all its values in (-1, 1) to a bytes data structure
    def float_byte_converter (self, array): 
        samp = self.samplewidth
        interm = array
        returned = bytes()
        for i in range(self.size):
            for k in range(self.nchannels):
                returned += int.to_bytes(int(interm[i, k]), samp, 'little') 
        return returned
    
    ## get_data_slice
    # @params: start_time (from which second do you want the data)
    # @params: end_time (until what seocnd should the data range)
    # returning a slice of the data in function of time
    def get_data_slice (self, start_time, end_time):
        print(start_time, end_time)
        print("here")
        print (self.data[(start_time*self.framerate):(self.framerate*end_time)])
        return np.array(self.data[int(self.framerate*start_time):int(self.framerate*end_time)])
                          
    ##########" private methods usefull for mixing 
                   
    def extend_with_zeroes_front (self, n):
        return np.concatenate((np.zeros((n, self.nchannels)), np.array(self.data)))
    
    def extend_with_zeroes_behind (self, n): 
        return np.concatenate((np.array(self.data), np.zeros((n, self.nchannels))))
                    
                    

    
    
        