
#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import time
import datetime
import shutil
import hashlib

import exifread
import exifread.exif_log

IMG_EXTS = ('.jpg','.jpeg')
class Imagefile(object):
    def __init__(self,path,filename):
        self.__filepath = path #文件路径      
        self.__filename = filename #文件名
        self.__full_file = os.path.join(self.__filepath,self.__filename) #构建完整文件路径
 
    def get_EXIF_datetime(self):
        fd = open(self.__full_file, 'rb')
        info = exifread.process_file(fd)
        if 'EXIF DateTimeOriginal' in info:
            t = info['EXIF DateTimeOriginal']
            t = str(t)
        else:
            t = '1981:01:01 00:00:00' #如果没有EXIF信息则认为9999年，便于后续处理
        fd.close()
        t = time.strptime(t,"%Y:%m:%d %H:%M:%S")
        return t

    # 获取某一个文件指纹    
    def get_fingerprint(self):
        file = open(self.__full_file,'rb').read()
        m = hashlib.md5(file)
        fingerprint = m.hexdigest()
        return fingerprint

    # 重命名
    def rename(self):        
        shortname,ext = os.path.splitext(self.__filename)
        data = self.get_EXIF_datetime()
        
        newshortname = str(data.tm_year)+'-'+str(data.tm_mon)+'-'+str(data.tm_mday) + shortname + ext.lower()
        #'-'+str(data.tm_hour)+"_"+
        #self.get_fingerprint()[:10]+ ext
        newfilename = os.path.join(self.__filepath,newshortname)
        # if ext in EXTS:
        try:
            os.rename(self.__full_file,newfilename)
        except Exception as e:
            print(e)
        finally:
            print('文件 %s 命名为 %s 成功' % (self.__full_file,newfilename))

def classify(path, newpath,video_path):
    # 根据文件的创建时间对文件分类
    for root, dirs, files in os.walk(path):
        for f in files:
            oldpath = os.path.join(root, f)
            one = Imagefile(root,f)
            # tm_year=2009, tm_mon=6, tm_mday=6, tm_hour=12, tm_min=12, tm_sec=24, tm_wday=5, tm_yday=157, tm_isdst=-1
            year = one.get_EXIF_datetime().tm_year 
            newpath_t = os.path.join(newpath, str(year))
            if os.path.splitext(f)[1].lower() not in IMG_EXTS:
                newpath_t = video_path 
            if not os.path.exists(newpath_t):
                os.makedirs(newpath_t)
                print('Create '+newpath_t+' success')
            newpath_full = os.path.join(newpath_t, f)
            print(newpath_full)
            shutil.copyfile(oldpath, newpath_full)  # 移动文件或文件夹

def remove_copy(src_dir):
    trash_path = src_dir+'_trash' #重复文件暂存
    if not os.path.exists(trash_path):
        os.mkdir(trash_path)
    tmp_fingerprint_list = []
    del_num = 0
    total_num = 0

    for dirpath,dirname,filenames in os.walk(src_dir):
        for filename in filenames:
            if  filename.startswith('.'):
                continue
            total_num += 1
            one = Imagefile(dirpath,filename)
            fingerprint = one.get_fingerprint()
            full_filename = os.path.join(dirpath,filename)
            if  fingerprint in tmp_fingerprint_list:
                print("重复文件：%s" % full_filename)
                del_num += 1
                try:
                    shutil.copyfile(full_filename,os.path.join(trash_path,filename))
                    os.remove(full_filename)
                    print('文件 %s 备份删除成功' % full_filename)   
                except Exception as e:
                    print(e)

            else:
                one.rename()
                tmp_fingerprint_list.append(fingerprint)

    print('总文件数：%d'%total_num)
    print('重复文件数:%d'%del_num)
    print('重复率：%.2f' % float(del_num/total_num))
if __name__ == "__main__":
    path = '/Users/linqing/Pictures/蛋蛋娃/add'
    newpath = '/Users/linqing/Pictures/pan.baidu/按年份_after_after'
    video_path = '/Users/linqing/Pictures/pan.baidu/video'
    #去重
    #remove_copy(path)
    #分类
    #classify(path, newpath,video_path)

