import os.path
from datetime import datetime

__author__ = 'Ken Chou'
__email__ = 'kenchou77@gmail.com'


def get_output_filename():
    return datetime.now().strftime('%Y-%m-%dT%H_%M_%S.h264')


def get_annotate(camera):
    return '{} {}@{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'x'.join([str(v) for v in camera.resolution]), camera.framerate)


def update_annotate(camera, interval):
    for i in range(0, interval):
        camera.annotate_text = get_annotate(camera)
        camera.wait_recording(1)


class DashCamera:
    def __init__(self, camera=None, **kwargs):
        """camera - instance of PiCamera"""
        self.camera = camera
        for k in kwargs:
            print(k, kwargs[k])

    def setup(self, **kwargs):
        pass

    def run(self):
        camera = self.camera
        storage_path = self.storage_path
        try:
            filename = get_output_filename()
            output_file = os.path.join(storage_path, filename)

            print('Start recording', filename)
            camera.start_preview()
            camera.start_recording(output_file, format='h264')
            # camera.annotate_text = get_annotate()
            # camera.wait_recording(interval)
            update_annotate(camera, self.interval)

            keep_going = True
            # main loop
            while keep_going:
                filename = get_output_filename()
                output_file = os.path.join(storage_path, filename)

                print('Start recording', filename)
                camera.split_recording(output_file)
                update_annotate(camera, self.interval)
                # camera.annotate_text = get_annotate()
                # camera.wait_recording(interval)
        except Exception as e:
            print(e)
        finally:
            print('Stop.')
            camera.stop_preview()
            camera.stop_recording()
            camera.close()
