#!/usr/bin/env python
# coding=utf-8
""" clean video storage path
"""
from time import sleep
from dashcamera import get_config
from dashcamera import VideoStorage


if __name__ == "__main__":
    config = get_config()
    storage_config = config['storage']
    storage_path = storage_config['path']
    video_storage = VideoStorage(storage_path)

    while True:
        for count in range(5):
            current_disk_usage = video_storage.get_disk_usage()
            if current_disk_usage < storage_config['max_disk_usage']:
                break
            print 'C:', current_disk_usage * 100
            remove_list = video_storage.delete_oldest_file()
            if remove_list:
                print("Removed: {}".format(remove_list))
            else:
                break
        sleep(60)
