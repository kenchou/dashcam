#!/usr/bin/env python3
""" clean video storage path
"""

import os
import yaml
from time import sleep
from dashcamera import VideoStorage


__author__ = 'Ken Chou <kenchou77@gmail.com>'


if __name__ == "__main__":
    config_file = os.path.join(os.path.dirname(__file__), 'etc/dashcam.yml')
    # print(config_file)
    with open(config_file, 'r') as stream:
        config = yaml.load(stream)
        # print(config)
        config['storage']['path'] = os.path.expanduser(config['storage']['path'])

    storage_config = config['storage']
    storage_path = storage_config['path']
    video_storage = VideoStorage(storage_path)

    while True:
        for count in range(5):
            current_disk_usage = video_storage.get_disk_usage()
            if current_disk_usage < storage_config['max_disk_usage']:
                break
            print('C:{:.2f}%'.format(current_disk_usage * 100), flush=True)
            remove_list = video_storage.delete_oldest_file()
            if remove_list:
                print("Removed: {}".format(remove_list))
            else:
                break
        sleep(60)
        print('.', end='', flush=True)
