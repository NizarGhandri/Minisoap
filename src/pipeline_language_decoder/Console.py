#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from signal import signal, SIGINT
from pipeline_language_decoder.Decoder import Decoder
import Preconditions as p
## Console
#
# This object is the console of the Minisoap that will take user's instructions
class Console():
    
    ## Console constructor
    #  @param self Object's pointer
    #  @param decoder Minisoap's decoder pointer
    def __init__(self, decoder):
        p.check_instance(decoder, Decoder, details="Decoder given not instance of decoder")
        self.decoder = decoder

    def run_instruction(self, instruction):
        try:
            self.decoder.transform(Decoder.grammar.parse(instruction))
        except Exception as e:
            print("ERROR in instruction")
            print(e)       
    ## @var decoder
    #  Minisoap's decoder pointer
    
    ## Console starting method
    #  @param self Object's pointer
    #  Enters an infinite loop (until stopped by the "stop" command) and take instructions from the user
    def start(self):
        #signal(SIGINT, self.quit)
        while(True):
            try:
                self.run_instruction(input("> "))
            except KeyboardInterrupt:
                print ("Exiting.")
                sys.exit()
