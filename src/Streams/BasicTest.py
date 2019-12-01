#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:49:29 2019

@author: nizar
"""

import sys
sys.path.append("../")                
from InputStream import InputStream as Input
from OutputStream import OutputStream as Output
from soundCard.OutputStreamSoundCard import OutputStream_SoundCard as out
from Track import Track
import libraries.operations as op
import libraries.generators as g


def add(seq1, seq2, a1=0.5, a2=0.5):
    return a1*seq1 + a2*seq2

def IO_Test ():
    wave1 = Input("samples/sanctuary.mp3")
    x = wave1.read_all()
    y = g.sine_t(500, 5, 440)
    z = op.crossfade_exp(x, y, 0.000001, 2)
    wave3 = out(z)
    wave3.write()
    wave1.close()
    #print(x.get_raw_data()[0, 44])
    #print(x.get_header())

if __name__ == "__main__": 
    IO_Test()