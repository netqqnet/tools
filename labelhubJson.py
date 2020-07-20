import requests
import json
import os
import sys
'''
labelHub网站的数据格式 如果没有质检则没有数据
'''
# 类别数
CLASSES = 6

def tagNameToId(name):
    # 给各类型编号
    name_list = [
        '饮料瓶', '酸奶牛奶盒', '易拉罐', '烟盒', '烟蒂', '玻璃', '塑料', '花草树枝树叶', '纸巾纸片',
        '口罩', '污水污渍', '泥土石块', '果皮', '打包垃圾', '堆放垃圾', '垃圾桶', '其它'
    ]
    # res_id = name_list.index(name)
    # 大致统计分类
    name_list = [
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

def labelHubToYolo():
    # 遍历文件夹 获取json文件
    json_file_path = '../../media/image/labelHub/'
    json_file_list = []
    for root, basename, files in os.walk(json_file_path):
        for file in files:
            file_path = os.path.join(root, file)
            json_file_list.append(file_path)
    for i in json_file_list:
        # 读取json文件
        with open(i, 'r', encoding='utf-8') as fp:
            obj_json = json.load(fp)
        # 读取json中的文件名称
        # json中的格式是 根路径[ {图片信息：}, {图片信息：}....]
        # 图片信息： {Data: {svgArr: [多目标标注信息]}, imagePath, imageWidth, imageHeight, imageName}
        # 标注信息： {data: [左上 右上 右下 左下标注点的{x, y}], name, }
        total_1 = len(obj_json)
        n = 0
        for i in obj_json:
            # 图片的网络地址
            image_path = i['imagePath']
            # 图片名称 宽度 高度
            image_name = i['imageName']
            image_width = i['imageWidth']
            image_height = i['imageHeight']
            pic_size = [image_width, image_height]
            if len(i['Data']) == 0:
                continue
            image_tag = i['Data']['svgArr']
            tag_info = []
            for j in image_tag:
                tag_name = j['name']
                tag_id = tagNameToId(tag_name)
                # 将坐标转为左上和右下坐标
                if len(j['data']) != 4:
                    continue
                box = [j['data'][0]['x'], j['data'][2]['x'], j['data'][0]['y'], j['data'][2]['y']]
                x, y, w, h = convert(pic_size, box)
                tag_info.append([tag_id, x, y, w, h])

            savePicText(image_name, image_path, tag_info)
            n += 1

if __name__ == '__main__':
    labelHubToYolo()