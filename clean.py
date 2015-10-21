#!/usr/bin/env python
# coding=utf-8
""" clean video storage path
"""
from time import sleep
import os.path
from dashcamera import get_config
from dashcamera import VideoStorage


if __name__ == "__main__":
    config_path = [os.path.abspath(os.path.join(os.path.dirname(__file__), 'etc'))]
    config = get_config(config_path=config_path)
    storage_config = config['storage']
    storage_path = storage_config['path']
    video_storage = VideoStorage(storage_path)

    print 'Dash Camera Storage Cleaner'
    print '==========================='
    print '* Storage Path:', storage_path
    print '*   Threshold:', storage_config['max_disk_usage']

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
