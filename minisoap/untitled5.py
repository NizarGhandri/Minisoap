#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 18:01:32 2020

@author: nizar
"""

from song import Song
from vumeter import Vumeter



s = Song("../songs/jingles/Squares.mp3")
v = Vumeter(s)

v.animate_track()
