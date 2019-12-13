import sys
import sounddevice as sd #low level library for soundcard(hardware) use
sys.path.append('../../')
import Preconditions as p
from Streams.Stream import Stream
from Streams.Tracks import Track 

## InputStream_SoundCard
#
# Input stream for sound card
class InputStream_SoundCard (Stream):
    
    ## InputStream_SoundCard constructor
    #  @param self Object's pointer
    #  @param nchannels Number of channels
    #  @param framerate The framerate
    #  @param dtype Format of data
    #  @param device Recording device
    #  @param infinite Boolean indicating if stream infinite
    #  @param launch Boolean indicating if input stream opened at initialization
    def __init__ (self, nchannels, framerate, dtype=sd.default.dtype, device= sd.default.device, infinite= True, launch = True):
        self.framerate = framerate
        self.nchannels = nchannels
        self.samplewidth = 0
        self.stream = sd.InputStream(samplerate=framerate, device = device, channels=nchannels, dtype=dtype)
        super().__init__(device, infinite, launch)
        
        
    ## Open method of sound card input stream
    #  @param self Object's pointer
    def open (self):
        self.launched = True
        self.stream.start()
        self.samplewidth = self.stream.samplesize
        
    ## Close method of sound card input stream
    #  @param self Object's pointer
    def close (self): 
        self.stream.stop()
        
    ## Read from soundcard
    #  @param self Object's pointer
    #  @param n number of frames
    #  @return a track containing the record
    def read(self, n):
        p.check(n <= self.time() and self.launched)
        return Track(self.stream.read(n)[0], n, self.nchannels, self.samplewidth, self.framerate)
    
    def read_available(self, n):
        return Track(self.stream.read_available(n)[0], n, self.nchannels, self.samplewidth, self.framerate)
    
    def time (self):
        return self.stream.time
        
        
            
        
        
        