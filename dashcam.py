#!/usr/bin/env python3
"""DashCam that using PiCamera"""

import os.path
import picamera
import dashcamera

__author__ = 'Ken Chou'
__email__ = 'kenchou77@gmail.com'


if __name__ == "__main__":
    storage_path = '/home/pi/Videos'
    interval = 3 * 60   # how many minutes every file
    resolution = (1920, 1080)    # Full HD
    # resolution = (1296, 972)
    keep_going = True

    with picamera.PiCamera() as camera:
        try:
            camera.resolution = resolution
            camera.framerate = 30
            camera.rotation = -90
            # camera.hflip = True
            # camera.vflip = True
            filename = dashcamera.get_output_filename()
            output_file = os.path.join(storage_path, filename)

            print('Start recording', filename)
            camera.start_preview()
            camera.start_recording(output_file, format='h264')
            # camera.annotate_text = get_annotate()
            # camera.wait_recording(interval)
            dashcamera.update_annotate(camera, interval)

            # main loop
            while keep_going:
                filename = dashcamera.get_output_filename()
                output_file = os.path.join(storage_path, filename)

                print('Start recording', filename)
                camera.split_recording(output_file)
                dashcamera.update_annotate(camera, interval)
                # camera.annotate_text = get_annotate()
                # camera.wait_recording(interval)
        except Exception as e:
            print(e)
        finally:
            print('Stop.')
            camera.stop_preview()
            camera.stop_recording()
            camera.close()
