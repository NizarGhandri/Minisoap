#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 16:04:15 2020

@author: nizar
"""

import pytest
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../..')
from src.Streams.InputStream import InputStream as Input
from src.Streams.OutputStream import OutputStream as Output
import hypothesis.strategies as st
from hypothesis import given
import subprocess
import numpy as np

def test_write_wav (): 
     wave1 = Input("Tests/test_samples/sanctuaryTest.wav")
     T = wave1.read_all()
     wave1.close()
     wave2 = Output("Tests/test_samples/testsample.wav", T)
     wave2.write()
     wave2.close()
     wave3 = Input("Tests/test_samples/testsample.wav")
     T_ = wave3.read_all()
     wave3.close()
     bashCommand = "rm Tests/test_samples/testsample.wav"
     process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
     output, error = process.communicate()
     assert np.array_equal(T.get_data(), T_.get_data())
     
     
def test_write_mp3 (): 
     wave1 = Input("Tests/test_samples/sanctuary.mp3")
     T = wave1.read_all()
     wave1.close()
     wave2 = Output("Tests/test_samples/testsample.wav", T)
     wave2.write()
     wave2.close()
     wave3 = Input("Tests/test_samples/testsample.wav")
     T_ = wave3.read_all()
     wave3.close()
     bashCommand = "rm Tests/test_samples/testsample.wav"
     process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
     output, error = process.communicate()
     assert np.array_equal(T.get_data(), T_.get_data())
