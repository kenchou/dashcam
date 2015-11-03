#!/usr/bin/env python
# coding=utf-8
"""DashCam that using PiCamera"""

import os.path
import picamera
import dashcamera


if __name__ == "__main__":
    config_path = [os.path.abspath(os.path.join(os.path.dirname(__file__), 'etc'))]
    config = dashcamera.get_config(config_path=config_path)
    storage_path = config['storage']['path']
    interval = config['video']['length']
    filename_pattern = config['video']['filename_pattern']
    encoder = config['video']['encoder']

    print 'Dash Camera'
    print '==========='
    print '* Storage Path:', storage_path
    print '* Interval    :', interval

    keep_going = True
    params = ['resolution', 'framerate', 'rotation', 'hflip', 'vflip']
    with picamera.PiCamera() as camera:
        try:
            dashcamera.set_config(camera, config)

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
