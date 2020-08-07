#import requests
import json
import os
import sys
'''
labelHub网站的数据格式 如果没有质检则没有数据
'''
# 类别数
CLASSES = 6

def tagNameToId(name):

    # 大致统计分类
    name_list_s = [
        '打包垃圾', '堆放垃圾', '垃圾桶', '果皮', '烟蒂', '其他'
    ]
    if name in name_list:
        res_id = name_list.index(name)
    else:
        res_id = 5
    return res_id

def convert(size, box):
    # size为图片的宽高 box矩形框的[左上x 右下x 左上y, 右下y]
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = round(x*dw, 6)
    w = round(w*dw, 6)
    y = round(y*dh, 6)
    h = round(h*dh, 6)
    return (x,y,w,h)

def downloadPic(pic_name, pic_path):
    # 下载图片
    img = requests.get(pic_path).content
    with open(pic_name, 'wb') as fp:
        fp.write(img)

def savePicText(pic_name, pic_path, tag_info):
    dir_path = '../../media/image/src'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    # 保存图片和txt
    txt_name = os.path.join(dir_path, pic_name.split('.')[0] + '.txt')
    pic_name = os.path.join(dir_path, pic_name)
    downloadPic(pic_name, pic_path)
    with open(txt_name, 'a') as fp:
        for i in tag_info:
            fp.write(' '.join([str(n) for n in i]))
            fp.write('\n')

def labelHubToYolo(json_file_path):
    # 遍历文件夹 获取json文件
    
    json_file_list = []
    filecount = 0
    for root, basename, files in os.walk(json_file_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.endswith('.json'):
                continue
            json_file_list.append(file_path)
    for i in json_file_list:
        # 读取json文件
        with open(i, 'r', encoding='utf-8') as fp:
            obj_json = json.load(fp)
        # 读取json中的文件名称
        # json中的格式是 根路径[ {图片信息：}, {图片信息：}....]
        for i in obj_json:
            filecount += 1
            if len(i['Data']) == 0:
                continue 
            image_tag = i['Data']['svgArr']           
            for j in image_tag:
                tag_name = j['name']
                if tag_name == '泥土':
                    tag_name = '泥土石块'
                tag_stat[name_list.index(tag_name)]+=1
    tag_stat_info=[]
    for each in range(len(tag_stat)):
        print("%s \t %d" % (name_list[each],tag_stat[each]))
    




if __name__ == '__main__':
    json_file_path = './data/labelhub'
    # 给各类型编号v
    name_list = [
        '饮料瓶', '酸奶牛奶盒', '易拉罐', '烟盒', '烟蒂', '玻璃', '塑料', '花草树枝树叶', '纸巾纸片',
        '口罩', '污水污渍', '泥土石块', '果皮', '打包垃圾', '堆放垃圾', '垃圾桶', '其它'
    ]
    tag_stat = [0 for i in range(len(name_list))]    
    labelHubToYolo(json_file_path)