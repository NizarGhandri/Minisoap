# Copyright (C) 2019 Mohamed H
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

from stream import Stream
from pathlib import Path
import  numpy, subprocess


## @var extensions
# Available songs extensions
extensions = ["wav", "mp3", "flac", "aac", "m4a", "ogg"]

## Song class
#
# Wrapper of a Song
class Song(Stream):
    
    def __init__(self, filename, chunk = None, samplerate = None, channels=None):
        self.path = Path(filename).absolute()
        Stream.__init__(self, chunk, samplerate, channels)
        if not self.path.suffix[1:] in extensions : raise Exception("Extension not supported")
        if not self.path.exists(): raise Exception("File not found")
    
    ## @var path
    # Path of the song
    
    ## Print the song
    #
    def __str__(self):
        return 'Song('+self.path.__str__()+')'
    
    ## Iterates over the song
    #
    def __iter__(self):
        self._t = 0.0
        p = subprocess.Popen(["ffmpeg", "-i", self.path, "-f", "f32le", "-acodec", "pcm_f32le",
                    "-ac", str(self.channels), "-ar", str(self.samplerate), "-"],
                    stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._pcmbuf = p.stdout
        return self
    
    ## Read next chunk
    #
    def __next__(self):
        a = self._pcmbuf.read(self.chunk*4*self.channels)
        if not len(a): raise StopIteration
        return numpy.frombuffer(a, dtype=numpy.float32).reshape((-1,self.channels))
        


