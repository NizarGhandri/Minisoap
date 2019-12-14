#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 18:56:05 2019

@author: nizar
"""
import sys 
sys.path.append("../")
import Preconditions as p
#import threading 
import matplotlib.pyplot as plt
#import numpy as np

class Vumeter: 
    
    
    approx_frames_per_sec = 88
    
    def __init__ (self, track=None, inputStreamSoundCard=None):
        tin = (track is None)
        iin = (inputStreamSoundCard is None)
        p.check(tin != iin)
        if (tin):
            self.source = inputStreamSoundCard
        elif (iin): 
            self.source = track
            
    ####fastest speed up possible to matplotlib is 500 frames per second thus 
    def animate_track (self):
        chunk_size = self.source.get_framerate()//self.approx_frames_per_sec + 1
        limit = self.source.get_size() - chunk_size
        fig, ax = plt.subplots()
        line, = ax.plot(self.source.get_data()[0:2*chunk_size, 0]/2**(8 * self.source.get_samplewidth()-1)-1)
        ax.set_ylim(-3, 3)
        plt.show(block=False)
        i = 0
        while i < limit:
            line.set_ydata(self.source.get_data()[i:i+2*chunk_size, 0]/2**(8 * self.source.get_samplewidth()-1)-1)
            fig.canvas.draw()
            fig.canvas.flush_events()
            i += chunk_size
        
        
        