import numpy as np
from Preconditions import *

def nullify(seq):
    return bytes([0 for k in seq])


def amplitude(seq, level):
    return bytes([level*k for k in seq])


def convolve(seq1, seq2):
    array1 = np.array([k for k in seq1])
    array2 = np.array([k for k in seq2])
    
    return bytes(np.convolve(array1, array2))


def add(seq1, seq2):
    return bytes([k for k in seq1] + [k for k in seq2])


def fade_exp(seq, factor):
    return bytes([seq[k]*factor^k for k in range(len(seq))])


def fade_lin(seq, speed):
    return bytes([seq[k] - speed*k for k in range(len(seq))])


def crossfade_exp(seq1, seq2, factor):
    return bytes([k for k in fade_exp(seq1, factor)] + [k for k in fade_exp(seq2, 1/factor)]
                  
                  
def crossfade_lin(seq1, seq2, speed):
    return bytes([k for k in fade_lin(seq1, speed)] + [k for k in fade_lin(seq2, -speed)])