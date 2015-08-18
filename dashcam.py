#!/usr/bin/env python

__author__ = 'kzhang'

import os.path
import picamera
from datetime import datetime


def get_output_filename():
    return datetime.now().strftime('%Y-%m-%dT%H_%M_%S.h264')


def get_annotate(camera):
    return '{} {}@{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'x'.join([str(v) for v in camera.resolution]), camera.framerate)


def update_annotate(camera, interval):
    for i in range(0, interval):
        camera.annotate_text = get_annotate(camera)
        camera.wait_recording(1)


storage_path = '/home/pi/Videos'
interval = 3 * 60   # how many minutes every file
resolution = (1920, 1080)    # Full HD
#resolution = (1296, 972)
keep_going = True

with picamera.PiCamera() as camera:
    try:
        camera.resolution = resolution
        camera.framerate = 30
        camera.rotation = -90
        #camera.hflip = True
        #camera.vflip = True
        filename = get_output_filename()
        output_file = os.path.join(storage_path, filename)

        print 'Start recording', filename
        camera.start_preview()
        camera.start_recording(output_file, format='h264')
        #camera.annotate_text = get_annotate()
        #camera.wait_recording(interval)
        update_annotate(camera, interval)

        # main loop
        while keep_going:
            filename = get_output_filename()
            output_file = os.path.join(storage_path, filename)

            print 'Start recording', filename
            camera.split_recording(output_file)
            update_annotate(camera, interval)
            #camera.annotate_text = get_annotate()
            #camera.wait_recording(interval)
    except Exception as e:
        print e
    finally:
        print 'Stop.'
        camera.stop_preview()
        camera.stop_recording()
        camera.close()

