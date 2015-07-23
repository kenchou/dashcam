#!/usr/bin/env python

__author__ = 'kzhang'

import picamera
from datetime import datetime


def get_output_filename():
    return datetime.today().strftime('%Y-%m-%d_%H_%M_%S.h264')


def get_annotate():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


interval = 5 * 60   # 5 minutes
resolution = (1920, 1080)    # Full HD
keep_going = True

with picamera.PiCamera() as camera:
    camera.resolution = resolution
    filename = get_output_filename()

    print 'Start recording', filename
    camera.start_recording(filename, format='h264')
    camera.annotate_text = get_annotate()
    camera.wait_recording(interval)

    # main loop
    while keep_going:
        filename = get_output_filename()
        print 'Start recording', filename
        camera.split_recording(filename)

        camera.annotate_text = get_annotate()
        camera.wait_recording(interval)

    print 'Stop.'
    camera.stop_recording()

