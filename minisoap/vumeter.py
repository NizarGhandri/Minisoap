#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 17:50:52 2020

@author: nizar
"""
import sys
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from stream import Stream

class Vumeter: 
    
    
    
    
    def __init__ (self, s):
        ## selecting the valid source 
        if not isinstance(s,Stream): raise TypeError
        self.traces = {}
        ## configuring the pyqtgraph
        self.s = s
        self.s.__iter__()
        pg.setConfigOptions(antialias=True)
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='Vumeter')
        self.win.setWindowTitle('Vumeter')
        self.win.setGeometry(5, 115, 1910, 1070)
        self.chunk = self.s.chunk
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
            self.waveform.setYRange(-1, 1, padding=0)
            self.waveform.setXRange(0, self.chunk, padding=0.005)

    def update(self):
        for i in range(self.s.channels):
            data= self.s.__next__()
            data = data[:,i]/np.max(data[:,i])
            self.set_plotdata(name=self.s.__str__(), data_x=self.x[0:len(data)], data_y=data,)

    def animate_track(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        refresh_time = int(self.chunk/self.s.samplerate*1000)+1
        timer.start(refresh_time)
        self.start()   
        