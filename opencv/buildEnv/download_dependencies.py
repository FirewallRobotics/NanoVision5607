# -----------------------------------------------------------------------------
# Name:         download_dependencies.py
# Purpose:      Script to read the conda list export file and download every dependency package in the list for all
#               available platforms
# Dependencies: requests, python 3.5
# -----------------------------------------------------------------------------

import requests
from pathlib import Path
import sys
import os

#region Gets path to environment file and downloads folder via command line
env_file = None
try:
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    if arg1 is not None:
        env_file = arg1
    else:
        env_file = 'arc_dependencies.txt'

    if arg2 is not None:
        channel_path = arg2
    else:
        file_path = os.path.dirname(os.path.realpath(__file__))
        channel_path = os.path.join(file_path, 'channel')
except:
    env_file = 'arcgis_v1_dependencies.txt'
    file_path = os.path.dirname(os.path.realpath(__file__))
    channel_path = os.path.join(file_path, 'channel')

print("Using environment list file: " + env_file)
print("File path is " + channel_path)
#endregion

#region Read env file:
path_list1 = []
with open(env_file, 'r') as env_file_handle:
    for line in env_file_handle.readlines():
        forward_path = line.replace('\\', '/')
        path_list1.append(forward_path)
#endregion

#region Download contents
for url in path_list1:
    p1 = url.rstrip('\n')
    path_splits = p1.split('/')
    file_name = path_splits[-1]

    print("Getting ", file_name)

    current_platform = path_splits[-2]
    platform_list = ['win-64', 'win-32', 'linux-64', 'linux-32', 'osx-32', 'osx-64']
    for platform in platform_list:
        p2 = p1.replace(current_platform, platform)
        download_folder = os.path.join(channel_path, platform)
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
            print("Created ", download_folder)

        download_file_path = os.path.join(channel_path, platform, file_name)
        if os.path.exists(download_file_path):
            os.remove(download_file_path)

        resp1 = requests.get(p2)
        if resp1.status_code == 200:
            with open(download_file_path, 'wb') as f_handle:
                f_handle.write(resp1.content)
                print('\t Downloaded {}\{}'.format(platform, file_name))
        else:
            print("\t Error with download: " + platform + " : " + resp1.__str__())

#endregion