## @defgroup preconditions Preconditions module
# 
# This module should contain all of the checking function that raise certain exceptions or errors. It will help modularise the code and make it cleaner all sort of checks can be added here.
# @{

# Include necessary imports here
import math as m
import sys
#from Streams.Tracks import Track


## Check method
#
#  @param value value to check
#  @param predicate the predicate
#  @param details comments
#  @exception ValueError
# The method check verifies if the value satisfies a certain predicate if not it raises a ValueError with details as specification of why value was wrong. 
def check(value, predicate=lambda x: x, details='bad value for this function'):
    if (not(predicate(value))): 
        raise ValueError(details)



## Check non None
#
#  @param value value to check
#  @param details comments
# The method check verifies if the value is not None
def check_non_none(value, details):
    check(value, predicate=lambda x: x is not None, details=details)


## Check instance
#
#  @param value value to check
#  @param instance_type the type to satisfy
#  @param details comments
# The method check verifies if the value is of type instance_type
def check_instance(value, instance_type, details):
    check(value, predicate=lambda x: isinstance(x, instance_type), details=details)



## Check in range
#
#  @param value value to check
#  @param startInclusive range start value
#  @param endInclusive range end value
# This method is a special case of check as it checks if a value is in a certain range or not.
def check_in_range(value, startInclusive=0, endExclusive= m.inf): 
    check(value, lambda x: x >= startInclusive and x < endExclusive)
    
    

## Check same parameters
#
#  @param track1 first track
#  @param track2 second track
# This method checks if two tracks have the same parameters
def check_same_params(track1, track2):
#    check_instance(track1, Track, "track given not instance of track")
#    check_instance(track2, Track, "track given not instance of track")
    get_params = lambda x: (x.get_nchannels(), x.get_samplewidth(), x.get_framerate())
    check((track1, track2), predicate=lambda x: get_params(x[0]) == get_params(x[1]), details="non compatible Tracks")

## error printing method   
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# @}
