#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:16:04 2019

@author: nizar
"""

import Preconditions as p
from Streams.Stream import Stream as s
import subprocess


class OutputStream (s): 
    
    writting_mode = 'wb'
       
    def __init__ (self, destination, track, launch = True): 
        super().__init__(destination, False, launch)
        self.wave_signal.setparams((track.get_nchannels(), track.get_samplewidth(), track.get_framerate(), track.get_size(), 'NONE', 'NONE'))
        self.track = track
    
    def open(self):
        super().open(OutputStream.writting_mode)
    
    def close(self):
        super().close()
        self.handle_format()
        
    def write (self):
        p.check(not(self.infinite), details ="cannot completly load an infinite stream")
        try: 
            return self.wave_signal.writeframesraw(self.track.get_raw_data())
        except:
            p.eprint("Error occured while writting the frames to destination", self.file)
            
    def set_as_stereo(self):
        p.check(self.launched, details ="cannot verify if stereo for unopened stream")
        self.wave_signal.setnchannels(2)
    
    def set_as_mono(self): 
        p.check(self.launched, details ="cannot verify if mono for unopened stream")
        self.wave_signal.setnchannels(1)
    
    def set_sample_width (self, n):
        p.check(self.launched, details ="cannot obtain sample width for unopened stream")
        self.wave_signal.setsampwidth(n)
    
    def set_frame_rate(self, n): 
        p.check(self.launched, details ="cannot obtain frame rate for unopened stream")
        self.wave_signal.setframerate(n)

    def set_size (self, n): 
        p.check(self.launched, details ="cannot return size of unopened stream")
        self.wave_signal.setnframes(n)
        
        
    def handle_format(self):
        
        if(self.file_format == "mp3"):
            old_path = self.file[:-3] + self.file_format
            bashCommand = "ffmpeg -nostats -loglevel 0 -i " + self.file + " " + old_path 
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        
        if(self.file_format != "wav"):
            bashCommand = "rm " + self.file
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        


        
        
    