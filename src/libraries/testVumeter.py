#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 14:54:25 2019

@author: nizar
"""



import Vumeter as v
import generators as g
import matplotlib.pyplot as plt
import time
import numpy as np

fig, ax = plt.subplots()
line, = ax.plot(np.random.randn(100))

tstart = time.time()
num_plots = 0
while time.time()-tstart < 1:
    line.set_ydata(np.random.randn(100))
    fig.canvas.draw()
    fig.canvas.flush_events()
    num_plots += 1
print(num_plots)

a = g.sine_t(1, 5, 440, nchannels = 1)
c = v.Vumeter(track = a)
#c.animate_track()




