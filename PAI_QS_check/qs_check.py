#!/usr/bin/env python
# -*- coding=utf-8 -*-
import io,os,json,cv2,random,time,numpy
from pypinyin import pinyin,lazy_pinyin 
from PIL import Image,ImageFont,ImageDraw
from fontTools import unicode

'''
为标注提供质检服务
Author: Ericlin
Update: 2020年11月25日
'''


manifest_file = '固定点位摊位识别_1606448285460.manifest'
#本地图片文件存放地址
local_file_sets = '/Users/linqing/Downloads/环卫数据/fixed-point_20201123'
sample_len = 100 #每次取样数量
label_id = 'label-ernztmy3piuz12nzei'
save_base_dir = '/Users/linqing/code/tools/PAI_QS_check/results/'
sub_dir = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
save_dir = os.path.join(save_base_dir,sub_dir)

def main():
    l = random_get(sample_len)
    for item in l:
        img_basename = os.path.basename(item['data']['picUrl'])
        img_path = os.path.join(local_file_sets,img_basename)
        labels = item[label_id]['results'][0]['data']
        image = cv2.imread(img_path)
        image = generate_img(image,labels)
        mkdir_if_not_exists(save_dir)
        os.chdir(save_dir)
        cv2.imwrite(img_basename,image)
        print(img_basename +' 生成成功!')

# 已经抽查的list
def checked_lib():
    lib = []
    for dirpath,dirname,filenames in os.walk(save_base_dir):
        for filename in filenames:
            if  filename.startswith('.'):
                continue
            lib.append(filename)
    return lib    


# 随机抽取
def random_get(sample_len):
    l = []
    lib = checked_lib()
    with open(manifest_file,'r',encoding='UTF-8') as f:
        for line in f.readlines():
            obj = json.loads(line)
            img_basename = os.path.basename(obj['data']['picUrl'])
            if label_id not in obj or img_basename in lib:
                print('跳过未标注或已经检查')
                continue
            else:
                l.append(obj)
    max_num = len(l)
    random.shuffle(l)
    print('随机取样成功')
    return l[:sample_len]


# 合成图片
def generate_img(image,labels):
    for item in labels:
        x = int(item['value']['x'])
        y = int(item['value']['y'])
        width = int(item['value']['width'])
        height= int(item['value']['height'])
        start_point = (x,y)
        end_point = (x + width,y + height)
        font_point = (x,y-40)
        color = (255,0,0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        #text = hanzi2pinyin(item['labels'][0])
        thickness = 2               
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
        image = put_hanzi_text(image,item['labels'][0],color,font_point)
    return image

# 汉字转拼音
def hanzi2pinyin(text):
    return ''.join(lazy_pinyin(text))

# 快捷函数 
def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)

# 图片上写汉字
def put_hanzi_text(img_cv,text,color,pos):
    img_PIL = Image.fromarray(cv2.cvtColor(img_cv,cv2.COLOR_BGR2RGB))
    if not isinstance(text,unicode):
        text = text.decode('utf-8')
    font_path = '/Users/linqing/code/tools/SimHei.ttf'
    font = ImageFont.truetype(font_path, 40)
    draw = ImageDraw.Draw(img_PIL)
    draw.text(pos,text,font=font,fill=color)
    img_cv = cv2.cvtColor(numpy.asarray(img_PIL),cv2.COLOR_RGB2BGR)
    return img_cv


if __name__ == "__main__":
    main()
