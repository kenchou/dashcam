#!/usr/bin/env python3
""" systemd
"""
import dashcamera
import yaml
import os

__author__ = 'Ken Chou'
__email__ = 'kenchou77@gmail.com'

if __name__ == "__main__":
    config_file = '/etc/dashcam.yml'
    # print(config_file)
    with open(config_file, 'r') as stream:
        config = yaml.load(stream)
        # print(config)
        config['storage']['path'] = os.path.expanduser(config['storage']['path'])

    controller = dashcamera.Controller(config=config)
    controller.run()
