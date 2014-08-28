#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
script_dir = os.getcwd()
script_dir = script_dir.replace('/bin', '')
sys.path.append(script_dir)

from lastmuse import last
tracks = last.fetch_tracks()

for i in range(len(tracks)):
    print "[%d] %s" % (i, tracks[i])
