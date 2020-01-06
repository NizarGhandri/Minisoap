#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 18:56:05 2019

@author: nizar
"""
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/..')

import Preconditions as p
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
#import threading 


class Vumeter: 
    
    
    chunk = 2048
    
    def __init__ (self, track=None, inputStreamSoundCard=None):
        ## selecting the valid source 
        tin = (track is None)
        iin = (inputStreamSoundCard is None)
        p.check(tin != iin)
        if (tin):
            self.source = inputStreamSoundCard
        elif (iin): 
            self.source = track
            self.normalized_data = self.source.get_data()/2**(8 * self.source.get_samplewidth())
        self.cursor = 0
        self.traces = {}
        ## configuring the pyqtgraph
        pg.setConfigOptions(antialias=True)
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='Vumeter')
        self.win.setWindowTitle('Vumeter')
        self.win.setGeometry(5, 115, 1910, 1070)
        self.x = np.arange(0, self.chunk, 1)
        half = self.chunk//2
        wf_xlabels = [(0, '0'), (half, str(half)), (self.chunk, str(self.chunk))]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (0.5, '0.5'), (1, '1')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        

        self.waveform = self.win.addPlot(
            title='WAVEFORM', row=1, col=1, axisItems={'bottom': wf_xaxis, 'left': wf_yaxis},
        )
            
# =============================================================================
#     ####fastest speed up possible to matplotlib is 500 frames per second thus 
#     def animate_track (self):
#         chunk_size = self.source.get_framerate()//self.approx_frames_per_sec + 1
#         limit = self.source.get_size() - chunk_size
#         fig, ax = plt.subplots()
#         line, = ax.plot(self.source.get_data()[0:2*chunk_size, 0]/2**(8 * self.source.get_samplewidth()-1)-1)
#         ax.set_ylim(-3, 3)
#         plt.show(block=False)
#         i = 0
#         while i < limit:
#             line.set_ydata(self.source.get_data()[i:i+2*chunk_size, 0]/2**(8 * self.source.get_samplewidth()-1)-1)
#             fig.canvas.draw()
#             fig.canvas.flush_events()
#             i += chunk_size
# =============================================================================
        
    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def set_plotdata(self, name, data_x, data_y):
        colour = 'c'
        if len(self.traces) % 2 == 1:
            colour = 'm'
            
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            self.traces[name] = self.waveform.plot(pen=colour, width=3)
            self.waveform.setYRange(0, 1, padding=0)
            self.waveform.setXRange(0, self.chunk, padding=0.005)

    def update(self):
        length = self.source.get_nchannels()
        for i in range(length):
            wf_data = self.normalized_data[self.cursor:self.cursor + self.chunk, i]
            self.set_plotdata(name='channel %d'%i, data_x=self.x[0:len(wf_data)], data_y=wf_data,)
        self.cursor += self.chunk

    def animate_track(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        refresh_time = int(self.chunk/self.source.get_framerate()*1000)+1
        timer.start(refresh_time)
        self.start()   
        
