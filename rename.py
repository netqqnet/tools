import os 
def filter_filenameAD(path,s):
    fileList = os.listdir(path)
    for file in fileList:
        used_fileName,extension = os.path.splitext(file)
        if (used_fileName.find(s) == -1):
            print("不用修改s%",used_fileName)
            continue       
        new_file =  used_fileName.replace(s,'') + extension;
        #new_file_path = os.path.join(path,new_file)
        os.rename(os.path.join(path,file) , os.path.join(path,new_file))
        print("文件%s重命名成功，新的文件名为：%s" %(path+file, path+new_file))
    
if __name__=='__main__':     
    path="/Users/linqing/Downloads/孙志立英语自然拼读100讲（完结）" 
   # s = "【公众号：花临同学，baozangku.ys168.com】"       #带过滤的广告
    s = '第'

   # path = os.getcwd()   # 获取当前目录
    filter_filenameAD(path,s)