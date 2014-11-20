#!/usr/bin/python3

from __future__ import print_function
from __future__ import unicode_literals

# Set the directory to the parent
import os
import sys
script_dir = os.path.realpath(__file__)
script_dir = script_dir.replace('/bin/cli.py', '')
sys.path.append(script_dir)

import subprocess


def run_vlc_unix(file_):

    if os.path.isfile('/usr/bin/vlc'):
        subprocess.call(['vlc', '-q', file_])
        return True

    else:
        return False


def run_vlc_win(file_):

    path_32 = r"C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
    path_64 = r"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"

    import subprocess
    if os.path.isfile(path_32):
        subprocess.call([path_32, file_])
        return True

    elif os.path.isfile(path_64):
        subprocess.call([path_64, file_])
        return True

    else:
        return False


def open_in_vlc(file):

    if os.name == 'nt':
        return run_vlc_win(file)

    elif os.name == 'posix':
        return run_vlc_unix(file)

    else:
        return False

from lastmuse import last
tracks = last.fetch_tracks()

try:
    if not tracks:
        print("FIXME: Tracks currently unavailable")
        sys.exit(-1)

    if len(sys.argv) < 2:

        for track in enumerate(tracks):
            print("[{:02d}] {} - {}".format(track[1].srl,
                                   track[1].artist,
                                   track[1].name))
    else:
        try:
            index = int(sys.argv[1]) - 1
        except ValueError:
            if sys.argv[1] == '--random' or sys.argv[1] == '-r':
                from random import randint
                index = randint(1, 20)

        # Check if the argument is in bounds
        if index < 0:
            index = 1
        elif index > 19:
            index = 19

        if len(sys.argv) > 2 and sys.argv[2] == "--sd":
            sd = True
        else:
            sd = False

        tracks[index].gen_url(hd=not sd)
        tracks[index].gen_lyrics()
        print("[{:02d}] {} - {}".format(tracks[index].srl,
                               tracks[index].artist,
                               tracks[index].name))
        print("--------")
        lyrics = tracks[index].lyrics
        try:
            print(lyrics)
        except UnicodeEncodeError:
            ascii_lyrics = ''.join([i if ord(i) < 128 else '' for i in lyrics])
            print(ascii_lyrics)
        # Open in VLC if installed otherwise in the browser
        if open_in_vlc(tracks[index].url):
            pass
        else:
            import webbrowser
            webbrowser.open(tracks[index].url)

except KeyboardInterrupt:
    print("GoodBye!")
