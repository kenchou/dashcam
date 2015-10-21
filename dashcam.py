#!/usr/bin/env python
# coding=utf-8
"""DashCam that using PiCamera"""

import os.path
import picamera
import dashcamera


if __name__ == "__main__":
    config = dashcamera.get_config()
    storage_path = config['storage']['path']
    interval = config['video']['length']
    filename_pattern = config['video']['filename_pattern']
    encoder = config['video']['encoder']

    keep_going = True

    params = ['resolution', 'framerate', 'rotation', 'hflip', 'vflip']
    with picamera.PiCamera() as camera:
        try:
            for key in config['camera']['params']:
                if key in params:
                    value = config['camera']['params'][key]
                    if key == 'resolution':
                        value = tuple([int(x) for x in value.lower().split('x')])
                    setattr(camera, key, value)

            filename = dashcamera.get_output_filename(pattern=filename_pattern)
            output_file = os.path.join(storage_path, filename)

            print 'Start recording', filename
            camera.start_preview()
            camera.start_recording(output_file, format=encoder)
            dashcamera.update_annotate(camera, interval)

            # main loop
            while keep_going:
                filename = dashcamera.get_output_filename(pattern=filename_pattern)
                output_file = os.path.join(storage_path, filename)

                print 'Start recording', filename
                camera.split_recording(output_file)
                dashcamera.update_annotate(camera, interval)

        except Exception as e:
            print e
        finally:
            print 'Stop.'
            camera.stop_preview()
            camera.stop_recording()
            camera.close()
