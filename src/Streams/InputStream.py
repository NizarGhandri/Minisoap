#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 00:49:13 2019

@author: nizar
"""
from Streams.Tracks import Track
import math as m
import Preconditions as p
from Streams.Stream import Stream as s
import subprocess

class InputStream(s): 
    reading_mode = 'rb'
    def __init__ (self, source, infinite = False, launch = True): 
        super().__init__(source, infinite, launch)
    
    #wave parameters: (nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed')
    def open(self):
        self.init_format()
        super().open(InputStream.reading_mode)
        self.wave_parameters = self.wave_signal.getparams()
        
    def close(self):
        super().close()
        self.end_format()
        
        
    def read_n_frames (self, n):
        p.check(self.launched, details ="cannot read unopened stream")
        p.check_in_range(n, endExclusive = self.get_size()+1)
        #try:
        return Track(self.wave_signal.readframes(n), n, nchannels = self.get_nchannels(), samplewidth = self.get_samplewidth(), framerate = self.get_framerate()) 
        #except:
            #p.eprint("Error occured while reading the frames from source", self.file)
            
            
    def read_all (self):
        p.check(not(self.infinite), details ="cannot completly load an infinite stream")
        return self.read_n_frames(self.get_size())
    
    def get_nchannels(self):
        return self.wave_parameters[0]
    
    def get_stereo(self):
        p.check(self.launched, details ="cannot verify if stereo for unopened stream")
        return self.wave_parameters[0] - 1
    
    def get_mono(self): 
        p.check(self.launched, details ="cannot verify if mono for unopened stream")
        return self.wave_parameters[0] % 2
    
    def get_samplewidth (self):
        p.check(self.launched, details ="cannot obtain sample width for unopened stream")
        return self.wave_parameters[1]
    
    def get_framerate(self): 
        p.check(self.launched, details ="cannot obtain frame rate for unopened stream")
        return self.wave_parameters[2]

    def get_size (self): 
        p.check(self.launched, details ="cannot return size of unopened stream")
        if (self.infinite):
            return m.inf
        else:
            return self.wave_parameters[3]
        
    def get_current_pos(self):
        p.check(self.launched, details ="cannot return pointer of unopened stream")
        return self.wave_signal.tell()
    
    def set_reading_pos (self, pos): 
        p.check(self.launched, details ="cannot modify pointer of unopened stream")
        p.check_in_range(pos, endExclusive=self.get_size())
        self.wave_signal.set(pos)
    
    
    ######### Handling file format
    
    ## Create temporary wav file
    def init_format(self):
        
        if(self.file_format == "mp3"):
            old_path = self.file[:-3] + self.file_format
            bashCommand = "ffmpeg -nostats -loglevel 0 -i " + old_path + " " + self.file
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        
    
    ## Remove temporary wav file
    def end_format(self):
        if(self.file_format != "wav"):
            bashCommand = "rm " + self.file
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        



        