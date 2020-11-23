import os,time
path = '/Users/linqing/Downloads'
for item in os.listdir(path):
    if not os.path.isdir(item):
        print(item)