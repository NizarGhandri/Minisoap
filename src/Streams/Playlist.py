
from Tools import format_path
from os import listdir
from os.path import isfile, join
import random
import libraries.operations as op
from Streams.InputStream import InputStream as Input
from functools import reduce 

class Playlist:
    def __init__(self, folderp="", merge=[]):
        p = folderp #format_path (folderp)
        print(p, folderp)
        l = listdir(p) if folderp != "" else [] 
        self.songs_paths = map(lambda x: p+x, [f for f in listdir(p) if isfile(join(p, f)) and f.split(".")[-1]=="wav"])
        for i in merge:
            for j in merge:
                self.songs_paths.append(j)
        self.transition = op.concat
    def get_songs_paths (self): return self.songs_paths
    def shuffle(self):
        random.shuffle (self.songs_paths)
    def set_transition(self, f):
        self.transition = f
    def to_track(self):
        return reduce(self.transition, map(lambda x: Input(x), self.songs_paths))
        


def merge_playlists(p1, p2):
    return Playlist(merge=[p1.get_songs_paths(),p2.get_songs_paths()])

class Fallback:
    pass
        
    