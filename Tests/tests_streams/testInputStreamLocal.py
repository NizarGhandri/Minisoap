#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 18:58:19 2019

@author: nizar
"""
import pytest
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../..')

from src.Streams.InputStream import InputStream as Input
import hypothesis.strategies as st
from hypothesis import given



#wave parameters: (nchannels, sampwidth, framerate, nframes, 'NONE', 'not compressed')
def test_open_wav ():
    wave1 = Input("Tests/test_samples/Alesis-Fusion-Bright-Acoustic-Piano-C2.wav")
    assert (wave1.get_nchannels(), wave1.get_sample_width(), wave1.get_frame_rate()) == (2, 2, 44100)
    wave1.close()

   
def test_open_mp3 ():
    wave1 = Input("Tests/test_samples/sanctuary.mp3")
    assert (wave1.get_nchannels(), wave1.get_sample_width(), wave1.get_frame_rate()) == (2, 2, 44100)
    wave1.close()

@given (st.integers())
def test_read_n (i): 
    wave1 = Input("Tests/test_samples/Alesis-Fusion-Bright-Acoustic-Piano-C2.wav")
    size = i % wave1.get_size()
    T = wave1.read_n_frames(size)
    assert T.get_size() == size
    wave1.close()
