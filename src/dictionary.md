# Commands dictionary

## Control Commands
* **execute** : Execute commands in pipeline
* **reset** : Reset pipeline
* **stop** : Stop program
* **show** : Show pipeline content
* **streams** : Show open streams
* **tracks** : Show available tracks
* **help** : Print command sheet

## Operation commands

### Main operations
* **open** *[file_path, file_id]* : Open new input stream at *file_path* and stores it with id *file_id*
* **close** *[file_id]* : Close input stream with id *file_id*
* **read** *[file_id, track_id, t="all"]* : Read t seconds of *file_id* and stores the track with *track_id* in the available tracks
* **write** *[file_path, track_id]* : Write the track with id *track_id* in *file_path*
* **free** *[track_id]* : Deletes the track with id *track_id* from available tracks
* **record** *[nchannels, framerate]* : Start recording from sound card
* **stop_record** *[track_id, nframes]* : Stop recording from sound card and store *nframes* frames in *track_id*
* **play** *[track_id]* : Start playing *track_id* from sound card
* **stop_play** *[]* : Stop playing from sound card

### Generators
* **sine** *[track_id, A, t, f, start=0, nchannels=2, samplewidth=2, fs=44100]* : Generate a sine wave with amplitude *A*, of length *t* in seconds and of frequency *f* and stores it in *track_id*
* **constant** *[track_id, t, value, start=0, nchannels=2, samplewidth=2, fs=44100]* : Generate a constant wave of value *value*, of length *t* in seconds and stores it in *track_id*
* **silence** *[track_id, t, start=0, nchannels=2, samplewidth=2, fs=44100]* : Generate a silent wave of length *t* in seconds and stores it in *track_id*

### Operations on tracks
* **nullify** *[track_id_in, track_id_out, start=0, end=None]* : Nullify the track *track_id_in* and stores it in *track_id_out*
* **fade** *[track_id_in, track_id_out, factor, t]* : Fade the track *track_id_in*, with factor *factor* starting from *t*, and stores it in *track_id_out*
* **fadeinv** *[track_id_in, track_id_out, factor, t]* : Fade inverse the track *track_id_in*, with factor *factor* starting from *t*, and stores it in *track_id_out*
* **amplitude** *[track_id_in, track_id_out, a]* : Multiply amplitude of the track *track_id_in* by a factor of *a* and stores it in *track_id_out*

* **crossfade** *[track_id_in1, track_id_in2, track_id_out, factor, t]* : Crossfade *track_id_in1* and *track_id_in2* with factor *factor* starting from *t*, and stores it in *track_id_out*
* **stereo** *[track_id_in1, track_id_in2, track_id_out]* : Join *track_id_in1* and *track_id_in2* in stereo and stores it in *track_id_out* (must have the same format)
* **mix** *[track_id_in1, track_id_in2, track_id_out, a1=0.5, a2=0.5]* : Mix *track_id_in1* with amplitude *a1* and *track_id_in2* with amplitude *a2* and stores it in *track_id_out*
* **convolve** *[track_id_in1, track_id_in2, track_id_out]* : Convolve *track_id_in1* and *track_id_in2* and stores it in *track_id_out*










 
