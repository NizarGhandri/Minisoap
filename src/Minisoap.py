#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:43:05 2019

@author: chris
"""

from pipeline_language_decoder.Decoder import Decoder
from processor.Processor import Processor
from pipeline_language_decoder.Console import Console


def main():
    processor = Processor()

    decoder = Decoder(processor)

    console = Console(decoder)

    console.start()
    
    
if __name__ == "__main__": 
    main()