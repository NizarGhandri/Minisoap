#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 14:54:25 2019

@author: nizar
"""



import Vumeter as v
import generators as g
import matplotlib.pyplot as plt
import numpy as np
from Streams.InputStream import InputStream as Input

K = Input("example.wav")
T = K.read_all()
a = g.sine_t(1, 5, 440, nchannels = 1)
c = v.Vumeter(track = a)
c.animate_track()




