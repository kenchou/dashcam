#!/usr/bin/env python3

__author__ = 'kzhang'

import shutil
import os
from time import sleep


video_storage_path = '.'  # TODO: get path from config
disk_usage_threshold = .85


class VideoStorage:
    def __init__(self, path):
        self.path = path
        self.video_files = []

    def get_video_files(self):
        current = os.getcwd()
        os.chdir(self.path)
        files = [f for f in os.listdir(self.path) if f.endswith('.h264') and os.path.isfile(os.path.join(self.path, f))]
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

        print ("  Deleted", filename)


video_storage = VideoStorage(video_storage_path)

while True:
    for count in range(1, 5):
        status = shutil.disk_usage(video_storage_path)
        disk_total = status[0]
        disk_used = status[1]
        disk_free = status[2]
        print('Disk usage:{:.2f}%'.format(disk_used / disk_total * 100))
        if disk_used / disk_total >= disk_usage_threshold:
            # remove oldest file
            video_storage.delete_oldest_file()
    sleep(30)
