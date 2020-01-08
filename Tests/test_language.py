#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 17:32:29 2019

@author: chris
"""
import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src')
from processor.Processor import Processor
from pipeline_language_decoder.Decoder import Decoder
from Streams.InputStream import InputStream
from Streams.Track import Track
import subprocess

def test_add_execute():
    processor = Processor()
    decoder = Decoder(processor)
    
    ## Open a dummy file
    instruction = "open [\"Tests/test_samples/sanctuary.wav\", \"test\"]"
    decoder.transform(Decoder.grammar.parse(instruction))
    
    assert not processor.pipeline.empty(), "Error in adding instruction to pipeline"
    
    decoder.transform(Decoder.grammar.parse("execute"))
    
    assert processor.pipeline.empty(), "execute not emptying pipeline"

    

def test_open_close():
    processor = Processor()
    decoder = Decoder(processor)
    
    ## Open
    instruction = "open [\"Tests/test_samples/sanctuary.wav\", \"test\"]"
    decoder.transform(Decoder.grammar.parse(instruction))
    decoder.transform(Decoder.grammar.parse("execute"))
    assert isinstance(processor.stream_in.get("test"), InputStream), "Fail to open file"
    
    ## Close
    instruction = "close [\"test\"]"
    decoder.transform(Decoder.grammar.parse(instruction))
    decoder.transform(Decoder.grammar.parse("execute"))
    
    assert processor.stream_in.get("test") is None
    

def test_reset():
    processor = Processor()
    decoder = Decoder(processor)
    
    ## Add dummy instructions    
    for i in range(10):
        decoder.transform(Decoder.grammar.parse("open [\"\"]"))
    
    decoder.transform(Decoder.grammar.parse("reset"))
    
    assert processor.pipeline.empty(), "Error in reset pipeline"
    


def test_read_free():
    
    processor = Processor()
    decoder = Decoder(processor)
    
    ## Open and read 2 seconds track
    decoder.transform(Decoder.grammar.parse("open [\"Tests/test_samples/sanctuary.wav\", \"test\"]"))
    decoder.transform(Decoder.grammar.parse("read [\"test\", \"track\", 2]"))
    decoder.transform(Decoder.grammar.parse("execute"))
    
    assert isinstance(processor.av_tracks.get("track"), Track), "Error in reading a track"
    
    assert abs(processor.av_tracks.get("track").get_time() - 2.0) < 1, "Error in reading a certain amount of seconds from a file" 
    
    decoder.transform(Decoder.grammar.parse("free [\"track\"]"))
    decoder.transform(Decoder.grammar.parse("execute"))
    
    assert processor.av_tracks.get("track") is None, "Free not emptying tracks"


def test_write():
    processor = Processor()
    decoder = Decoder(processor)
    
    ## Open and read 2 seconds track
    decoder.transform(Decoder.grammar.parse("open [\"Tests/test_samples/sanctuary.wav\", \"test\"]"))
    decoder.transform(Decoder.grammar.parse("read [\"test\", \"track\"]"))
    decoder.transform(Decoder.grammar.parse("execute"))
    
    decoder.transform(Decoder.grammar.parse("write [\"Tests/test_samples/out.wav\", \"track\"]"))
    decoder.transform(Decoder.grammar.parse("execute"))
    
    decoder.transform(Decoder.grammar.parse("open [\"Tests/test_samples/out.wav\", \"test2\"]"))
    decoder.transform(Decoder.grammar.parse("read [\"test2\", \"track2\"]"))
    decoder.transform(Decoder.grammar.parse("execute"))
    
    assert processor.av_tracks.get("track").get_raw_data() == processor.av_tracks.get("track2").get_raw_data(), "Writing and reading have different values"
    
    command = "rm Tests/test_samples/out.wav"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
        











 
    
    
