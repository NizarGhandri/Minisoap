# Minisoap
A modular audio processor

# Project Description: 
An audio stream processor that can create and transform audio streams,
featuring basic synthesis capabilities as well as file and soundcard I/O.
It is designed modularly, allowing the user to specify its own processing pipeline.

# Instructions for use

## About the doc
Run index.html in the html folder. Doc generated with doxygen with configurations in src/doxyconfig

## About the language
The language dictionary with instructions on how to use every operations can be found in src/dictionary.md

## Launch Minisoap
```
python src/Minisoap.py
```

## Example of pipeline
open ["Streams/samples/sanctuary.wav", "sanctuary_stream"]<br/>
read ["sanctuary_stream", "sanctuary_track", 2]<br/>
show<br/>
execute<br/>
streams<br/>
amplitude ["sanctuary_track", "track_out1", 0.8]<br/>
sine ["sine_track1", 1, 3, 440]<br/>
sine ["sine_track2", 1, 3, 40]<br/>
mix ["sine_track1", "sine_track2", "track_out2", 3]<br/>
tracks<br/>
write ["ex1.wav", "track_out1"]<br/>
write ["ex2.wav", "track_out2"]<br/>
stop<br/>
