# coding=utf-8

from __future__ import division
import os
from datetime import datetime


def get_config(config_path=['/etc']):
    import yaml
    config_exists = False
    for search_path in config_path:
        config_file = os.path.abspath(os.path.join(search_path, 'dashcam.yml'))
        if os.path.isfile(config_file):
            config_exists = True
            break
    if not config_exists:
        raise IOError('Config does not exists in %s' % ','.join(config_path))
    with open(config_file, 'r') as stream:
        config = yaml.load(stream)
        config['storage']['path'] = os.path.expanduser(config['storage']['path'])
    return config


def get_output_filename(pattern='%Y-%m-%dT%H_%M_%S', ext_name='h264'):
    return datetime.now().strftime('%s.%s' % (pattern, ext_name))


def get_annotate(camera):
    return '{} {}@{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                             'x'.join([str(v) for v in camera.resolution]),
                             camera.framerate)


def update_annotate(camera, interval):
    for i in range(0, interval):
        camera.annotate_text = get_annotate(camera)
        camera.wait_recording(1)


class VideoStorage:
    def __init__(self, path):
        self.path = path
        # file list cache
        self.video_files = []

    def get_disk_usage(self):
        stat = os.statvfs(self.path)
        disk_total = stat.f_blocks * stat.f_bsize
        disk_avail = stat.f_bavail * stat.f_bsize
        return (disk_total - disk_avail) / disk_total

    def get_video_files(self):
        current = os.getcwd()
        os.chdir(self.path)
        files = [os.path.join(self.path, f) for f in os.listdir(self.path)
                 if f.endswith('.h264') and os.path.isfile(os.path.join(self.path, f))]
        os.chdir(current)
        sorted_list = sorted(files, key=os.path.getmtime)
        return sorted_list

    def delete_oldest_file(self):
        if not self.video_files:
            self.video_files = self.get_video_files()
        if not self.video_files:
            return []

        oldest = self.video_files.pop(0)
        filename, extension = os.path.splitext(oldest)

        base = os.path.join(self.path, filename)

        check_list = ['.jpg', '.h264', '.mp4']
        remove_list = []
        for ext in check_list:
            filename = base + ext
            if os.path.exists(filename):
                remove_list.append(filename)
                os.remove(filename)
        return remove_list
