#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 18:58:19 2019

@author: nizar
"""
import sys
import pytest
#import hypothesis.strategies as st
sys.path.append("../../")
from src.Streams.InputStream import InputStream as Input

#wave parameters: (nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed')
def test_open_wav ():
    wave1 = Input("samples/Alesis-Fusion-Bright-Acoustic-Piano-C2.wav")
    assert (wave1.get_nchannels(), wave1.get_samplewidth(), wave1.get_framerate()) == (2, 2, 44100)

    




