#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/..')

import queue as Queue
from Streams.InputStream import InputStream as Input
import libraries.generators as g
from Streams.OutputStream import OutputStream as Output
import libraries.operations as op
import sounddevice as sd
from Streams.soundCard.InputStreamSoundCard import InputStream_SoundCard
from Streams.soundCard.OutputStreamSoundCard import OutputStream_SoundCard
import Preconditions as p
from libraries.Vumeter import Vumeter

## Processor
#
# This object is the processor of the Minisoap that will execute commands
class Processor():
    
    ## Processor constructor
    #  @param self Object's pointer
    def __init__(self):
        self.pipeline = Queue.Queue()
        
        self.stream_in = {}
        self.stream_out = {}
        self.av_tracks = {}
        
    ## @var pipeline
    #  Pipeline of instructions
    
    ## @var stream_in
    #  Dictionary containing opened input streams
    
    ## @var stream_out
    #  Dictionary containing opened output streams
    
    ## @var av_tracks
    #  Available tracks for manipulation
    
    
    
    
    ## Add operation to pipeline
    #
    #  @param op The operation
    #  @param args The arguments
    def add(self, op, args):
        self.pipeline.put((op, args))
    
    
    def execute(self):
        """!
        Execute commands in pipeline
        """
        if(self.pipeline.empty()):
            print("Pipeline empty, fill in instructions!")
        else:
            while not self.pipeline.empty():
                op, args = self.pipeline.get()
                try:
                    op(*args)
                except Exception as e:
                    print("Error in instruction " + op.__name__ + " " + str(args))
                    print(e)
            
            
    def reset(self):
        """!
        Reset pipeline
        """
        self.pipeline = Queue.Queue()
        self.pipeline_print = Queue.Queue()
    
    
    def stop(self):
        """!
        Stop the program
        """
        print("STOP")
        exit(0)

    def tracks(self):
        """!
        Show available tracks
        """
        print(self.av_tracks)
        
    def streams(self):
        """!
        Show available streams
        """
        print(self.stream_in)
        
    def show(self):
        """!
        Show pipeline content
        """
        if(self.pipeline.empty()):
            print("Pipeline empty")
    
        for q_item in self.pipeline.queue:
            print(q_item[0].__name__ + " " + str(q_item[1]) + "\n")
    
    ##def helpp(self):
   ##     """!
   ##     Print available operations
   ##     """
   ##     print("######################################## HELP ########################################")
   ##     with open('help.txt', 'r') as fin:
   ##         print(fin.read())
           
    
    def openn(self, file_path, file_id):
        """!
        Open input stream
        
        open [file_path, file_id]
        
        @param file_path Input Stream file path
        @param file_id Id with which the input stream will be stored
        
        Open new input stream at *file_path* and stores it with id *file_id*
        """
        stream = Input(file_path)
        self.stream_in.update({file_id: stream})
        
    
    def close(self, file_id):
        """!
        Close input stream
        
        close [file_id]
        
        @param file_id Id of the input stream to be closed
        
        Close input stream with id *file_id*
        """
        s = self.stream_in.pop(file_id)
        if (s is not None):
            s.close()
        
        
    def read(self, file_id, track_id, t="all"):
        """!
        Read track from input stream
        
        read [file_id, track_id, t="all"]
        
        @param file_id Id of the input stream
        @param track_id Id to store the track
        @param t Time in seconds to read from file (default all)
    
        Read t seconds of *file_id* and stores the track with *track_id* in the available tracks
        """
        if(t == "all"):
            s = self.stream_in.pop(file_id)
            p.check_non_none(s, details="Invalid stream ID")
            track = s.read_all()
            s.close()
        else: 
            s = self.stream_in.get(file_id)
            p.check_non_none(s, details="Invalid stream ID")
            fs = s.frame_rate()
            track = s.read_n_frames(int(float(t)*fs))
        self.av_tracks.update({track_id: track})
        
    
    def write(self, file_path, track_id):
        """!
        Write track in output stream
        
        write [file_path, track_id]
        
        @param file_path path of the output file
        @param track_id Id of the track to be written
    
        Write the track with id *track_id* in *file_path*
        """
        track = self.av_tracks.get(track_id)
        p.check_non_none(track, details="Invalid track ID")
        stream = Output(file_path, track)
        stream.write()
    
    
    def free(self, track_id):
        """!
        Delete a track
        
        free [track_id]
        
        @param track_id Id of the track to be deleted
        
        Deletes the track with id *track_id* from available tracks
        """
        self.pop(track_id)
    
    
    def record(self, nchannels, framerate, device=sd.default.device):
        """!
        Start recording from soundcard
        
        record [nchannels, framerate]
        
        @param nchannels number of channels
        @param framerate framerate
        @param device device from which to record (check sounddevice library to change default value)
        
        Start recording from sound card
        """
        sd = InputStream_SoundCard(nchannels, framerate, device=device)
        self.stream_in.update({"soundcard" : sd})
    
    
    def stop_record(self, track_id, nframes):
        """!
        Stop recording from soundcard
        
        stop_record [track_id, nframes]
        
        @param track_id: Id of track to store result
        @param nframes number of frames to store
        
        Stop recording from sound card and store *nframes* frames in *track_id*
        """
        sd = self.stream_in.pop("soundcard")
        p.check_non_none(sd, details="Sound card not opened")
        self.av_tracks.update({track_id : sd.read(nframes)})
        sd.close()
        
    
    def play(self, track_id, device=sd.default.device):
        """!
        Play track from soundcard
        
        play [track_id, device=sd.default.device]
        
        @param track_id Id of track to be played
        @param device device from which to play (check sounddevice library to change default value)
        
        Start playing *track_id* from sound card
        """
        
        track = self.av_tracks.get(track_id)
        p.check_non_none(track, details="Invalid track ID")
        
        sd = OutputStream_SoundCard(track, device=device)
        sd.write()
        self.stream_out.update({"soundcard" : sd})
        
    
    def stop_play(self):
        """!
        stop_play []
        
        Stop playing from sound card
        """
        sd = self.stream_in.pop("soundcard")
        p.check_non_none(sd, details="Sound card not opened")
        sd.close()
    
    
    
    def sine(self, track_id, A, t, f, start = 0, nchannels = 2, samplewidth =2, fs = 44100): #last four agrs are optional 
        """!
        Generate sine wave
        
        sine [track_id, A, t, f, start=0, nchannels=2, samplewidth=2, fs=44100]
        
        @param track_id Id of the track
        @param A amplitude
        @param t duration in seconds
        @param f frequency
        @param start second when to start
        @param nchannels number of channels
        @param samplewidth samplewidth
        @param fs sampling frequency
        
        Generate a sine wave with amplitude *A*, of length *t* in seconds and of frequency *f* and stores it in *track_id*
        """
        self.av_tracks.update({track_id: g.sine_t(A, t, f, start = start, nchannels = nchannels,  samplewidth = samplewidth, fs = fs)})
        
    
    
    def constant(self, track_id, t, value, start = 0, nchannels = 2, samplewidth = 2, fs=44100):
        """!
        Generate a constant wave
        
        constant [track_id, t, value, start=0, nchannels=2, samplewidth=2, fs=44100]
        
        @param track_id Id of the track
        @param t duration in seconds
        @param value amplitude
        @param start second when to start
        @param nchannels number of channels
        @param samplewidth samplewidth
        @param fs sampling frequency
        
        Generate a constant wave of value *value*, of length *t* in seconds and stores it in *track_id*
        """
        self.av_tracks.update({track_id: g.constant_t(t, value, start = start, nchannels = nchannels, samplewidth = samplewidth, fs=fs)})
        
    
    def silence(self, track_id, t, start = 0, nchannels = 2, samplewidth = 2, fs=44100):
        """!
        Generate a silent wave
        
        silence [track_id, t, start=0, nchannels=2, samplewidth=2, fs=44100]
        
        @param track_id Id of the track
        @param t duration in seconds
        @param start second when to start
        @param nchannels number of channels
        @param samplewidth samplewidth
        @param fs sampling frequency
        
        Generate a silent wave of length *t* in seconds and stores it in *track_id*
        """
        self.constant(track_id, t, 0, start = start, nchannels = nchannels, samplewidth = samplewidth, fs=fs)
        
    
    def nullify(self, track_id_in, track_id_out, start=0, end=None):
        """!
        Nullify a track
        
        nullify [track_id_in, track_id_out, start=0, end=None]
        
        @param track_id_in Id of input track
        @param track_id_out Id of output track
        @param start second when to start
        @param end second when to end
    
        Nullify the track *track_id_in* and stores it in *track_id_out*
        """
        track = self.av_tracks.get(track_id_in)
        p.check_non_none(track, details="Invalid track ID")
        self.av_tracks.update({track_id_out : op.nullify(track, start, end)})


    def fade(self, track_id_in, track_id_out, factor, t):
        """!
        Fade a track
        
        fade [track_id_in, track_id_out, factor, t]
        
        @param track_id_in Id of input track
        @param track_id_out Id of output track
        @param factor fading factor
        @param t second when to start the fade

        Fade the track *track_id_in*, with factor *factor* starting from *t*, and stores it in *track_id_out*
        """
        track = self.av_tracks.get(track_id_in)
        p.check_non_none(track, details="Invalid track ID")
        self.av_tracks.update({track_id_out : op.fade_exp(track, factor, t)})

    
    def fadeinv(self, track_id_in, track_id_out, factor, t):
        """!
        Fade inverse a track
        
        fadeinv [track_id_in, track_id_out, factor, t]
        
        @param track_id_in Id of input track
        @param track_id_out Id of output track
        @param factor fading factor
        @param t second when to start the fade
        
        Fade inverse the track *track_id_in*, with factor *factor* starting from *t*, and stores it in *track_id_out*
        """
        track = self.av_tracks.get(track_id_in)
        p.check_non_none(track, details="Invalid track ID")
        self.av_tracks.update({track_id_out : op.fade_inv(track, factor, t)})

    
    def amplitude(self, track_id_in, track_id_out, a):
        """!
        Multiply amplitude of a track
        
        amplitude [track_id_in, track_id_out, a]
        
        @param track_id_in Id of input track
        @param track_id_out Id of output track
        @param a multiplying factor
        
        Multiply amplitude of the track *track_id_in* by a factor of *a* and stores it in *track_id_out*
        """
        track = self.av_tracks.get(track_id_in)
        p.check_non_none(track, details="Invalid track ID")
        self.av_tracks.update({track_id_out : op.amplitude(track, a)})


    def stereo(self, track_id_in1, track_id_in2, track_id_out):
        """!
        Combine two tracks in stereo (must have the same properties)
        
        stereo [track_id_in1, track_id_in2, track_id_out]
        
        @param track_id_in1 Id of first input track
        @param track_id_in2 Id of second input track
        @param track_id_out Id of output track
    
        Join *track_id_in1* and *track_id_in2* in stereo and stores it in *track_id_out* (must have the same format)
        """
        track1 = self.av_tracks.get(track_id_in1)
        track2 = self.av_tracks.get(track_id_in2)
        p.check_non_none(track1, details="Invalid first track ID")
        p.check_non_none(track2, details="Invalid second track ID")
        self.av_tracks.update({track_id_out : op.mono_to_stereo(track1, track2)})


    def crossfade(self, track_id_in1, track_id_in2, track_id_out, factor, t):
        """!
        Crossfade two tracks
        
        crossfade [id_track_in1, track_id_in2, track_id_out, factor, t]
        
        @param track_id_in1 Id of first input track
        @param track_id_in2 Id of second input track
        @param track_id_out Id of output track
        @param factor fading factor
        @param t second when to start the fade
        
        Crossfade *track_id_in1* and *track_id_in2* with factor *factor* starting from *t*, and stores it in *track_id_out*
        """
        track1 = self.av_tracks.get(track_id_in1)
        track2 = self.av_tracks.get(track_id_in2)
        p.check_non_none(track1, details="Invalid first track ID")
        p.check_non_none(track2, details="Invalid second track ID")
        self.av_tracks.update({track_id_out : op.crossfade_exp(track1, track2, factor, t)})


    def mix(self, track_id_in1, track_id_in2, track_id_out, t, a1=0.5, a2=0.5):
        """!
        Mix two tracks
        
        mix [track_id_in1, track_id_in2, track_id_out, a1=0.5, a2=0.5]
        
        @param track_id_in1 Id of first input track
        @param track_id_in2 Id of second input track
        @param track_id_out Id of output track
        @param t second when to start the fade
        @param a1 amplitude of first track
        @param a2 amplitude of second track
   
        Mix *track_id_in1* with amplitude *a1* and *track_id_in2* with amplitude *a2* and stores it in *track_id_out*
        """
        track1 = self.av_tracks.get(track_id_in1)
        track2 = self.av_tracks.get(track_id_in2)
        p.check_non_none(track1, details="Invalid first track ID")
        p.check_non_none(track2, details="Invalid second track ID")
        self.av_tracks.update({track_id_out : op.add(track1, track2, t, a1, a2)})


    def convolve(self, track_id_in1, track_id_in2, track_id_out):
        """!
        Convolve two tracks
        
        convolve [track_id_in1, track_id_in2, track_id_out]
        
        @param track_id_in1 Id of first input track
        @param track_id_in2 Id of second input track
        @param track_id_out Id of output track
    
        Convolve *track_id_in1* and *track_id_in2* and stores it in *track_id_out*
        """
        track1 = self.av_tracks.get(track_id_in1)
        track2 = self.av_tracks.get(track_id_in2)
        p.check_non_none(track1, details="Invalid first track ID")
        p.check_non_none(track2, details="Invalid second track ID")
        self.av_tracks.update({track_id_out : op.convolve(track1, track2)})


    def vumeter(self, track_id):
        """!
        Vumeter
        
        vumeter [track_id]
        
        @param track_id Id of track
        
        Visualize track using Vumeter
        """
        track = self.av_tracks.get(track_id)
        v = Vumeter(track=track)
        v.animate_track()
        
        
        
        
        
        