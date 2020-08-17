#coding:utf-8

import os,time
import hashlib
import shutil

"""
1.以md5方式重命名指定目录；
2.把获取到指纹写入txt文件；
3.查询并去除重复文件

推荐业务处理流程：
1.

"""
#某文件
class OneImage(object):
    
    def __init__(self,path,filename):
        self.__filepath = path #目标文件路径      
        self.__filename = filename #目标文件名
        self.__full_file = os.path.join(self.__filepath,self.__filename) #构建完整文件路径
        self.__exts = ('.jpg','.jpeg','.png')
   
    # 获取某一个文件指纹    
    def get_fingerprint(self):
        file = open(self.__full_file,'rb').read()
        m = hashlib.md5(file)
        fingerprint = m.hexdigest()
        return fingerprint
                  
    # 重命名
    def rename(self):        
        shortname,ext = os.path.splitext(self.__filename)
        newshortname = self.get_fingerprint() + ext
        newfilename = os.path.join(self.__filepath,newshortname)
        if ext in self.__exts:
            try:
                os.rename(self.__full_file,newfilename)
            except Exception as e:
                print(e)
            finally:
                print('文件 %s 命名为 %s 成功' % (self.__full_file,newfilename))       

# 指纹库 
class FingerprintLib(object):
    
    def __init__(self,fingerprint_lib_dir):
        self.__fingerprint_lib_dir = fingerprint_lib_dir #指纹库路径


    # 指纹库中检查是否重复，重复返回true
    def is_has(self,str):
        ls = [f for f in os.listdir(fingerprint_lib_dir) if f.endswith('.lock')]
        stock_fingerprint_lib = []
        for item in ls:
            with open(os.path.join(self.__fingerprint_lib_dir,item),'r',encoding='utf-8') as f:
                for line in f.readlines():
                    stock_fingerprint_lib.append(line.strip())
        return str in stock_fingerprint_lib
              

    # 添加指纹库 输入list
    def add(self,l):
        filename = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        suffix = '.txt'
        full_filename = os.path.join(self.__fingerprint_lib_dir,filename+suffix)
        if not os.path.exists(full_filename):
            with open(os.path.join(full_filename),'w',encoding='utf-8') as f:
                for item in l:
                    f.write(str(item)+"\n")

    # 指纹库唯一性检查
    def check_unique(self):
        pass


# 
def conversion(src_dir,fingerprint_lib_dir):
    trash_path = src_dir+'_trash' #重复文件暂存
    if not os.path.exists(trash_path):
        os.mkdir(trash_path)
    tmp_fingerprint_list = []
    lib = FingerprintLib(fingerprint_lib_dir)
    del_num = 0
    total_num = 0

    for dirpath,dirname,filenames in os.walk(src_dir):
        for filename in filenames:
            if  filename.startswith('.'):
                continue
            total_num += 1
            one = OneImage(dirpath,filename)
            fingerprint = one.get_fingerprint()
            full_filename = os.path.join(dirpath,filename)
            if  lib.is_has(fingerprint) or (fingerprint in tmp_fingerprint_list):
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
    lib.add(tmp_fingerprint_list)
    print('总文件数：%d',total_num)
    print('重复文件数:%d',del_num)
    print('重复率：%.2f',del_num/total_num)

                
if __name__ == '__main__':
    
    src_dir = '/Users/linqing/Downloads/环卫数据/第二批次/2020年08月11日的副本'
    fingerprint_lib_dir = '/Users/linqing/Downloads/环卫数据/fingerprint-lib/'    
    conversion(src_dir,fingerprint_lib_dir)

    
