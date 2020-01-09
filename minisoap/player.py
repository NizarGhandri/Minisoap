# Copyright (C) 2020 Mohamed H
# 
# This file is part of Minisoap.
# 
# Minisoap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Minisoap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Minisoap.  If not, see <http://www.gnu.org/licenses/>.

from .killable_thread import KillableThread
from .stream import Stream
import soundcard as sc
import time
from .microphone import Microphone

## Player class
#
# A stream player
class Player(KillableThread):
    def __init__(self, stream):
        if not isinstance(stream, Stream): raise TypeError
        KillableThread.__init__(self)
        self.stream = stream
        self.is_mic = isinstance(self.stream, Microphone)
        self._play = True
        self.sp = sc.default_speaker()
        self._stop = False
            
    ## @var stream
    # Stream to be played
    
    ## @var _play
    # Boolean indicating if playing
    
    ## @var sp
    # Spreakers (default value of soundcard library)
    
    ## @var stop
    # Boolean indicating if the player is stopped
    
    ## Run the player
    #
    def run(self):
        with self.sp.player(samplerate=self.stream.samplerate,
            channels=self.stream.channels) as sp:
            for block in self.stream:
                while not self._play:
                    if self.killed(): return
                    time.sleep(0.1)
                if self.killed(): break
                sp.play(block)

    ## Pause the player
    #
    def pause(self):
        self._play = False
    
    ## Play the player
    #
    def play(self):
        self._play = True