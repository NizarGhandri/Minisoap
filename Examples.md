# Example

```
open ["Streams/samples/sanctuary.wav", "sanctuary_stream"]
read ["sanctuary_stream", "sanctuary_track", 2]
show
execute
streams
amplitude ["sanctuary_track", "track_out1", 0.8]
sine ["sine_track1", 1, 3, 440]
sine ["sine_track2", 1, 3, 40]
mix ["sine_track1", "sine_track2", "track_out2", 3]
tracks
write ["ex1.wav", "track_out1"]
write ["ex2.wav", "track_out2"]
stop
```
