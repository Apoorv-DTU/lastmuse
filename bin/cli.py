#!/usr/bin/python3

from __future__ import print_function
from __future__ import unicode_literals

# Set the directory to the parent
import os
import sys
script_dir = os.getcwd()
script_dir = script_dir.replace('/bin', '')
sys.path.append(script_dir)

from lastmuse import last
tracks = last.fetch_tracks()

if len(sys.argv) < 2:

    for track in enumerate(tracks):
        print("[{}] {}".format(track[1].srl, track[1].name))
else:
    index = int(sys.argv[1]) - 1

    # Check if the argument is in bounds
    if index < 0:
        index = 1
    elif index > 19:
        index = 19

    tracks[index].gen_url()
    tracks[index].gen_lyrics()
    print("[{}] {}: {}".format(tracks[index].srl,
                               tracks[index].name,
                               tracks[index].url))
    print("--------")
    print(tracks[index].lyrics)
