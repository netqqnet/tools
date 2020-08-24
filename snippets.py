#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os

''' 
常用函数和snippets
Author: Ericlin
Update:2020年08月24日
''' 

a = '1,2,3,4'
[float(i) for i in a.split(',')]

# Operating system flag
# Note: Somes libs depends of OS
is_bsd = sys.platform.find('bsd') != -1
is_linux = sys.platform.startswith('linux')
is_mac = sys.platform.startswith('darwin')
is_windows = sys.platform.startswith('win')



class ObjectDict(dict):
    """Makes a dictionary behave like an object."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value
# d = {'a':1,'b':2}
# o  = ObjectDict(d)


class Workstatus(Enum):
    ''' 
    # 定义常量
    '''
    nowork = 0  # 不工作
    scan = 1  # 巡检模式
    clean = 2  # 清扫模式



def file_2_lst(file_path,separator = ':'):
    ''' 
    # 按行读取文件，返回list
    '''    
    l = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            if line == '\n':
                continue
            if separator is not None:   
                _l = line.split(separator)
            else:
                _l = line            
            l.append(_l)
    return l


# 把内容写入文件
def content2file(content, path, filename, mode='w'):
    
    mkdir_if_not_exists(path)
    with open(path+filename, mode) as f:
        f.write(content)
        f.write('\n')


# does not operate recursively
def list_directories(directory, exclude_prefixes=('.',)):
    for f in os.listdir(directory):
        if f.startswith(exclude_prefixes):
            continue
        joined = os.path.join(directory, f)
        if os.path.isdir(joined):
            yield joined

# extensions can be a string or list, can include the preceding . or not
# operates recursively
def list_files(directory, extensions=None, exclude_prefixes=('.',)):
    if type(extensions) == str:
        extensions = [extensions]
    if extensions is not None:
        extensions = [('' if e.startswith('.') else '.') + e for e in extensions]
    for root, dirnames, filenames in os.walk(directory):
        filenames = [f for f in filenames if not f.startswith(exclude_prefixes)]
        dirnames[:] = [d for d in dirnames if not d.startswith(exclude_prefixes)]
        for filename in filenames:
            base, ext = os.path.splitext(filename)
            joined = os.path.join(root, filename)
            if extensions is None or ext.lower() in extensions:
                yield joined


def file_count(path,ignore_set=(['.DS_Store'])):
    count = 0
    for root,dirs,files in os.walk(path):    #遍历统计
        for f in files:
            if  f.endswith('.DS_Store'):
                continue
            count = count + 1  #统计文件夹下文件个数
    return count





# 快捷函数 
def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_datetime(formt='%Y%m%d%H%M%S'):
    dt = time.strftime(formt, time.localtime(time.time()))
    return dt

def  is_ds_store(f):
    '''
    mac专用
    '''
    flag = False
    if f.endswith('.DS_Store'):
        flag = True
    return flag