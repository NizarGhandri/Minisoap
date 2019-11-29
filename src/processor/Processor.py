#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import queue as Queue
from Streams.InputStream import InputStream as Input
import libraries.generators as g
from Streams.OutputStream import OutputStream as Output
import libraries.operations as op
import sounddevice as sd
from Streams.soundCard.InputStreamSoundCard import InputStream_SoundCard
from Streams.soundCard.OutputStreamSoundCard import OutputStream_SoundCard
import Preconditions as p

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
    
    
    
    ###################################################### CONTROL OPERATIONS
    
    ## Add operation to pipeline
    #
    #  @param self Object's pointer
    #  @param op The operation
    #  @param args The arguments
    def add(self, op, args):
        self.pipeline.put((op, args))
    
    
    ## Execute the pipeline
    #
    #  @param self Object's pointer
    def execute(self):
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
            
            
    ## Reset the pipeline
    #
    #  @param self Object's pointer
    def reset(self):
        self.pipeline = Queue.Queue()
        self.pipeline_print = Queue.Queue()
    
    
    ## Stop the program
    #
    #  @param self Object's pointer
    def stop(self):
        print("STOP")
        exit(0)

    ## Print available tracks to stdout
    #
    #  @param self Object's pointer
    def tracks(self):
        print(self.av_tracks)
        
    ## Print opened input streams to stdout
    #
    #  @param self Object's pointer
    def streams(self):
        print(self.stream_in)
        
    ## Print pipeline to stdout
    #
    #  @param self Object's pointer
    def show(self):
        if(self.pipeline.empty()):
            print("Pipeline empty")
    
        for q_item in self.pipeline.queue:
            print(q_item[0].__name__ + " " + str(q_item[1]) + "\n")
    
    ## Print help sheet to stdout
    #
    #  @param self Object's pointer
    def helpp(self):
        print("######################################## HELP ########################################")
        with open('help.txt', 'r') as fin:
            print(fin.read())
           
    ###################################################### OPERATIONS
    
    
    ################# MAIN OPERATIONS
    
    ## Open input stream
    #
    #  @param self Object's pointer
    #  @param file_path Input Stream file path
    #  @param file_id Id with which the input stream will be stored
    def openn(self, file_path, file_id):
        stream = Input(file_path)
        self.stream_in.update({file_id: stream})
        
    ## Close input stream
    #
    #  @param self Object's pointer
    #  @param file_id Id of the input stream to be closed
    def close(self, file_id):
        s = self.stream_in.pop(file_id)
        if (s is not None):
            s.close()
        
        
    ## Read track from input stream
    #
    #  @param self Object's pointer
    #  @param file_id Id of the input stream
    #  @param track_id Id to store the track
    #  @param t Time in seconds to read from file (default all)
    def read(self, file_id, track_id, t="all"):
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
        
    ## Write track in output stream
    #
    #  @param self Object's pointer
    #  @param file_path path of the output file
    #  @param track_id Id of the track to be written
    def write(self, file_path, track_id):
        track = self.av_tracks.get(track_id)
        p.check_non_none(track, details="Invalid track ID")
        stream = Output(file_path, track)
        stream.write()
    
    ## Delete a track
    #
    #  @param self Object's pointer
    #  @param track_id Id of the track to be deleted
    def free(self, track_id):
        self.pop(track_id)
    
    ## Start recording from soundcard
    #
    #  @param self Object's pointer
    #  @param nchannels number of channels
    #  @param framerate framerate
    #  @param device device from which to record (check sounddevice library to change default value)
    def record(self, nchannels, framerate, device=sd.default.device):
        sd = InputStream_SoundCard(nchannels, framerate, device=device)
        self.stream_in.update({"soundcard" : sd})
    
    ## Stop recording from soundcard
    #
    #  @param self Object's pointer
    #  @param track_id Id of track to store result
    #  @param nframes number of frames to store
    def stop_record(self, track_id, nframes):
        sd = self.stream_in.pop("soundcard")
        p.check_non_none(sd, details="Sound card not opened")
        self.av_tracks.update({track_id : sd.read(nframes)})
        sd.close()
        
    ## Play track from soundcard
    #
    #  @param self Object's pointer
    #  @param track_id Id of track to be played
    #  @param device device from which to play (check sounddevice library to change default value)
    def play(self, track_id, device=sd.default.device):
        track = self.av_tracks.get(track_id)
        p.check_non_none(track, details="Invalid track ID")
        sd = OutputStream_SoundCard(track, device=device)
        sd.write()
        self.stream_out.update({"soundcard" : sd})
        
    ## Stop playing from soundcard
    #
    #  @param self Object's pointer
    def stop_play(self):
        sd = self.stream_in.pop("soundcard")
        p.check_non_none(sd, details="Sound card not opened")
        sd.close()
    
    ################# GENERATOR OPERATIONS
    
    
    ## Generate sine wave
    #
    #  @param self Object's pointer
    #  @param track_id Id of the track
    #  @param A amplitude
    #  @param t duration in seconds
    #  @param f frequency
    #  @param start second when to start
    #  @param nchannels number of channels
    #  @param samplewidth samplewidth
    #  @param fs sampling frequency
    def sine(self, track_id, A, t, f, start = 0, nchannels = 2, samplewidth =2, fs = 44100): #last four agrs are optional 
        self.av_tracks.update({track_id: g.sine_t(A, t, f, start = start, nchannels = nchannels,  samplewidth = samplewidth, fs = fs)})
        
    ## Generate constant wave
    #
    #  @param self Object's pointer
    #  @param track_id Id of the track
    #  @param t duration in seconds
    #  @param value value of wave
    #  @param start second when to start
    #  @param nchannels number of channels
    #  @param samplewidth samplewidth
    #  @param fs sampling frequency
    def constant(self, track_id, t, value, start = 0, nchannels = 2, samplewidth = 2, fs=44100):
        self.av_tracks.update({track_id: g.constant_t(t, value, start = start, nchannels = nchannels, samplewidth = samplewidth, fs=fs)})
        
    ## Generate silent wave
    #
    #  @param self Object's pointer
    #  @param track_id Id of the track
    #  @param t duration in seconds
    #  @param start second when to start
    #  @param nchannels number of channels
    #  @param samplewidth samplewidth
    #  @param fs sampling frequency
    def silence(self, track_id, t, start = 0, nchannels = 2, samplewidth = 2, fs=44100):
        self.constant(track_id, t, 0, start = start, nchannels = nchannels, samplewidth = samplewidth, fs=fs)
        
    ################# OPERATIONS ON TRACKS
    
    ## Nullify a track
    #
    #  @param self Object's pointer
    #  @param track_id_in Id of input track
    #  @param track_id_out Id of output track
    #  @param start second when to start
    #  @param end second when to end
    def nullify(self, track_id_in, track_id_out, start=0, end=None):
        track = self.av_tracks.get(track_id_in)
        p.check_non_none(track, details="Invalid track ID")
        self.av_tracks.update({track_id_out : op.nullify(track, start, end)})


        
    ## Fade a track
    #
    #  @param self Object's pointer
    #  @param track_id_in Id of input track
    #  @param track_id_out Id of output track
    #  @param factor fading factor
    #  @param t second when to start the fade
    def fade(self, track_id_in, track_id_out, factor, t):
        track = self.av_tracks.get(track_id_in)
        p.check_non_none(track, details="Invalid track ID")
        self.av_tracks.update({track_id_out : op.fade_exp(track, factor, t)})

    ## Fade inverse a track
    #
    #  @param self Object's pointer
    #  @param track_id_in Id of input track
    #  @param track_id_out Id of output track
    #  @param factor fading factor
    #  @param t second when to start the fade
    def fadeinv(self, track_id_in, track_id_out, factor, t):
        track = self.av_tracks.get(track_id_in)
        p.check_non_none(track, details="Invalid track ID")
        self.av_tracks.update({track_id_out : op.fade_inv(track, factor, t)})

    ## Multiply amplitude of a track
    #
    #  @param self Object's pointer
    #  @param track_id_in Id of input track
    #  @param track_id_out Id of output track
    #  @param a multiplying factor
    def amplitude(self, track_id_in, track_id_out, a):
        track = self.av_tracks.get(track_id_in)
        p.check_non_none(track, details="Invalid track ID")
        self.av_tracks.update({track_id_out : op.amplitude(track, a)})


    ## Combine two tracks in stereo (must have the same properties)
    #
    #  @param self Object's pointer
    #  @param track_id_in1 Id of first input track
    #  @param track_id_in2 Id of second input track
    #  @param track_id_out Id of output track
    def stereo(self, track_id_in1, track_id_in2, track_id_out):
        track1 = self.av_tracks.get(track_id_in1)
        track2 = self.av_tracks.get(track_id_in2)
        p.check_non_none(track1, details="Invalid first track ID")
        p.check_non_none(track2, details="Invalid second track ID")
        self.av_tracks.update({track_id_out : op.mono_to_stereo(track1, track2)})


    ## Crossfade two tracks
    #
    #  @param self Object's pointer
    #  @param track_id_in1 Id of first input track
    #  @param track_id_in2 Id of second input track
    #  @param track_id_out Id of output track
    #  @param factor fading factor
    #  @param t second when to start the fade
    def crossfade(self, track_id_in1, track_id_in2, track_id_out, factor, t):
        track1 = self.av_tracks.get(track_id_in1)
        track2 = self.av_tracks.get(track_id_in2)
        p.check_non_none(track1, details="Invalid first track ID")
        p.check_non_none(track2, details="Invalid second track ID")
        self.av_tracks.update({track_id_out : op.crossfade_exp(track1, track2, factor, t)})


    ## Mix two tracks
    #
    #  @param self Object's pointer
    #  @param track_id_in1 Id of first input track
    #  @param track_id_in2 Id of second input track
    #  @param track_id_out Id of output track
    #  @param t second when to start the fade
    #  @param a1 amplitude of first track
    #  @param a2 amplitude of second track
    def mix(self, track_id_in1, track_id_in2, track_id_out, t, a1=0.5, a2=0.5):
        track1 = self.av_tracks.get(track_id_in1)
        track2 = self.av_tracks.get(track_id_in2)
        p.check_non_none(track1, details="Invalid first track ID")
        p.check_non_none(track2, details="Invalid second track ID")
        self.av_tracks.update({track_id_out : op.add(track1, track2, t, a1, a2)})


    ## Convolve two tracks
    #
    #  @param self Object's pointer
    #  @param track_id_in1 Id of first input track
    #  @param track_id_in2 Id of second input track
    #  @param track_id_out Id of output track
    def convolve(self, track_id_in1, track_id_in2, track_id_out):
        track1 = self.av_tracks.get(track_id_in1)
        track2 = self.av_tracks.get(track_id_in2)
        p.check_non_none(track1, details="Invalid first track ID")
        p.check_non_none(track2, details="Invalid second track ID")
        self.av_tracks.update({track_id_out : op.convolve(track1, track2)})

