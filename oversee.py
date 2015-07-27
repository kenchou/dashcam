#!/usr/bin/env python3

__author__ = 'kzhang'

import shutil
import os

path = '.'  # TODO: get path from config
disk_usage_threshold = .9


def delete_oldest_file(path):
    # Deletes oldest file in a specified directory
    current = os.getcwd()
    os.chdir(path)
    files = sorted(os.listdir(path), key=os.path.getmtime)
    oldest = files[0]
    os.chdir(current)
    filename, extension = os.path.splitext(oldest)

    print(filename, extension)

    base = os.path.join(path, filename)
    # if os.path.exists(base + '.jpg'):
    #     os.remove(base + '.jpg')
    #
    # if os.path.exists(base + '.h264'):
    #     os.remove(base + '.h264')
    #
    # if os.path.exists(base + '.mp4'):
    #     os.remove(base + '.mp4')

    print ("  Deleted", base)


while True:
    status = shutil.disk_usage(path)
    disk_total = status[0]
    disk_usage = status[1]
    disk_free = status[2]
    if disk_free / disk_total >= disk_usage_threshold:
        break
    # remove oldest file
    delete_oldest_file(path)