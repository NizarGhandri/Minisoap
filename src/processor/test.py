#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 23:38:33 2020

@author: chris
"""

import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../..')
import src.libraries.generators as g
from src.libraries.Vumeter import Vumeter
from Streams.soundCard.OutputStreamSoundCard import OutputStream_SoundCard
from threading import Thread


track = g.sine_t(1, 10, 440, nchannels=1)
v = Vumeter(track=track)
v.animate_track()