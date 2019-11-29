#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 19:55:58 2019

@author: chris
"""

from pipeline_language_decoder.Decoder import Decoder
from processor.Processor import Processor
from pipeline_language_decoder.Console import Console


processor = Processor()

decoder = Decoder(processor)

console = Console(decoder)

console.start()



## TESTS
sine ["sine", 2, 5, 60]

open ["Streams/samples/sanctuary.mp3", "sanctuary"]
read ["sanctuary", "track1", 2]

sine ["sine", 2, 5, 60]
sine ["null", 2, 5, 60]

nullify["null", "null"]

fade ["track1", "fade", 0.5, 1]
write ["faded.wav", "fade"]

amplitude ["sine", "sine", 10]


#### ERRORS
stereo ["track1", "sine", "stereo"]
mix ["fade", "track1", "mix", 10]
