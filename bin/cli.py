#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
script_dir = os.getcwd()
script_dir = script_dir.replace('/bin', '')
sys.path.append(script_dir)

from lastmuse import last
tracks = last.fetch_tracks()

if len(sys.argv) < 2:

    for i in range(len(tracks)):
        print "[%d] %s" % (i+1, tracks[i])

else:
    index = int(sys.argv[1]) - 1
    url = last.vimeo_url_from_track(tracks[index])
    print "[%d] %s: %s" % (index, tracks[index], url)
