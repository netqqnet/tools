import os
import shutil

# 对目标路径下所有的文件合并，并且按照step大小分别存放
def dirsplit(path,step = 3000):
    if not os.path.exists(path):
        print("目录不存在")
        return
    new_path_dir = os.path.join(path,"new")   
    i=0
    filesCount = 0  
    for root,dirs,files in os.walk(path):
        for f in files:
            if  f.endswith('.DS_Store'):
                continue
            (shotname, extension) = os.path.splitext(f)
            old_path = os.path.join(root, f) 
            i = i+1          
            if i%step == 1 and len(files)>step:
               filesCount = filesCount +1
               new_path_dir = os.path.join(new_path_dir,"0000"+str(filesCount))                         

            if not os.path.exists(new_path_dir):
                os.makedirs(new_path_dir) 
            new_path =os.path.join(new_path_dir,f)

            try:
                shutil.copyfile(old_path,new_path)
                print("%s copyed" % old_path)
            except IOError as e:
                print('fail')
        print("总共拷贝%s" % i)
    
def delFiles(path):
  for root , dirs, files in os.walk(path):
    for f in files:
      if f.endswith(".jpg"):  
        os.remove(os.path.join(root, f))
        print ("Delete File: " + os.path.join(root, f))

def fileStat(path):
    count = 0
    for root,dirs,files in os.walk(path):    #遍历统计
        for f in files:
            if  f.endswith('.DS_Store'):
                continue
            count = count + 1  #统计文件夹下文件个数
    print(count)  # 输出结果


if __name__ == "__main__":
    path = '/Users/linqing/Downloads/环卫数据/'
    #dirsplit(path)
    fileStat(path)
