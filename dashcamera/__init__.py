import os.path
from datetime import datetime
import multiprocessing
from time import sleep
import sys
import shutil

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


class PiCameraWorker(multiprocessing.Process):
    def __init__(self, name=None, config=None, options=None):
        super().__init__(name=name)
        self.config = config
        self.options = options

    def run(self):
        # print(self.args)
        print('    ├── In %s(%s)' % (self.name, self.pid))
        if hasattr(os, 'getppid'):  # only available on Unix
            print('    │          ppid:', os.getppid())

        storage_path = self.options['storage']['path']
        interval = self.options['video']['length']
        encoder = self.options['video']['encoder']
        import picamera

        keep_going = True
        camera = picamera.PiCamera()
        try:
            for k in self.config['params']:
                v = self.config['params'][k]
                if k == 'resolution':
                    v = tuple([int(x) for x in v.split('x')])
                setattr(camera, k, v)

            filename = get_output_filename()
            output_file = os.path.join(storage_path, filename)

            print('Start recording', filename)
            camera.start_preview()
            camera.start_recording(output_file, format=encoder)
            # camera.annotate_text = get_annotate()
            # camera.wait_recording(interval)
            update_annotate(camera, interval)

            # main loop
            while keep_going:
                filename = get_output_filename()
                output_file = os.path.join(storage_path, filename)

                print('Start recording', filename)
                camera.split_recording(output_file)
                update_annotate(camera, interval)
                # camera.annotate_text = get_annotate()
                # camera.wait_recording(interval)
        except Exception as e:
            print(e)
        finally:
            print('Stop.')
            camera.stop_preview()
            camera.stop_recording()
            camera.close()


class Cleaner(multiprocessing.Process):
    def __init__(self, name=None, config=None):
        super().__init__(name=name)
        self.config = config

    def run(self):
        print('    ├── In %s(%s)' % (self.name, self.pid))
        if hasattr(os, 'getppid'):  # only available on Unix
            print('    │          ppid:', os.getppid())
        storage_path = self.config['path']
        video_storage = VideoStorage(storage_path)

        while True:
            for count in range(1, 5):
                current_disk_usage = video_storage.get_disk_usage()
                if current_disk_usage < self.config['max_disk_usage']:
                    break
                print('C:{:.2f}%'.format(current_disk_usage * 100))
                video_storage.delete_oldest_file()
            print('.', end='')
            sys.stdout.flush()
            sleep(30)


class Controller:
    """ Dash Camera Controller
    """
    def __init__(self, config=None):
        """ camera - instance of PiCamera
            storage_path - video storage path
            interval - how many seconds every file
        """
        self.config = config
        self.cameras = []
        self.jobs = []

    def attach(self, camera):
        if camera not in self.cameras:
            self.cameras.append(camera)

    def detach(self, camera):
        if camera in self.cameras:
            self.cameras.remove(camera)

    def run(self):
        # add cleaner worker
        # video_storage = VideoStorage(self.config['storage']['path'])
        p = Cleaner(config=self.config['storage'])
        self.jobs.append(p)

        options = {'storage': self.config['storage'], 'video': self.config['video']}
        camera_enabled = self.config['camera']['enabled']
        cameras = [c for c in self.config['camera']['device'] if c['name'] in camera_enabled]
        for device in cameras:
            p = PiCameraWorker(name=device['name'], config=device, options=options)
            self.jobs.append(p)

        for p in self.jobs:
            p.start()

        running = True
        while running:
            running = False
            for p in self.jobs:
                running = running or p.is_alive()
            sleep(1)
        print('DONE!')


class VideoStorage:
    def __init__(self, path):
        self.path = path
        self.video_files = []

    def get_disk_usage(self):
        status = shutil.disk_usage(self.path)
        disk_total = status[0]
        disk_used = status[1]
        return disk_used / disk_total

    def get_video_files(self):
        current = os.getcwd()
        # print('Current Path:', current)
        os.chdir(self.path)
        # print('Now chdir:', os.getcwd())
        files = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith('.h264') and os.path.isfile(os.path.join(self.path, f))]
        os.chdir(current)
        sorted_list = sorted(files, key=os.path.getmtime)
        return sorted_list

    def delete_oldest_file(self):
        if not self.video_files:
            self.video_files = self.get_video_files()
        if not self.video_files:
            print('Empty file list. delete nothing.')
            return

        oldest = self.video_files.pop(0)
        filename, extension = os.path.splitext(oldest)

        base = os.path.join(self.path, filename)
        if os.path.exists(base + '.jpg'):
            os.remove(base + '.jpg')

        if os.path.exists(base + '.h264'):
            os.remove(base + '.h264')

        if os.path.exists(base + '.mp4'):
            os.remove(base + '.mp4')

        print("  Deleted", filename)
