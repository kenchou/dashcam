#!/usr/bin/env python

__author__ = 'kzhang'

import subprocess
from picamera import PiCamera


# Run a viewer with an appropriate command line. Uncomment the mplayer
# version if you would prefer to use mplayer instead of VLC
cmdline = ['cvlc', 'stream:///dev/stdin', '--sout', '#standard{access=http,mux=ts,dst=:8554}', ':demux=h264']
player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

with PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 30

    camera.start_recording(player.stdin, format='h264', quality=23)
    while True:
        camera.wait_recording(1)
