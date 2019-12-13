#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:43:05 2019

@author: chris
"""

from pipeline_language_decoder.Decoder import Decoder
from processor.Processor import Processor
from pipeline_language_decoder.Console import Console
from Tools import format_path
import sys

def main(instructions):
    processor = Processor()

    decoder = Decoder(processor)

    console = Console(decoder)

    for i in instructions:
        console.run_instruction(i)

    console.start()
    
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = format_path(sys.argv[1])
        with open(path, 'r') as f:
            main(f.read().split("\n"))

    else: main([])