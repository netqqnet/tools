#!/usr/bin/env python
# encoding: utf-8
from kafka import KafkaProducer
from kafka.errors import KafkaError
import cv2
import numpy as np
import setting,common

conf = setting.kafka_setting
log = common.log
# 接口协议约定的 https://hsgm.coding.net/p/huanweiai/wiki/1
#  唯一ID /str / 是 / 识别结果和相关数据对应
#  采集时间 /unixtime/ 是 / 该视频帧的实际时间
#  视频一帧数据/cvMat/ 是  / Opencv格式的cvMat矩阵数据
#  工作模式/int / 是 / 清扫模式或巡检模式
#  其他数据/dict /否 / 需要上报的其他数据


def getGPS():
    pass 

def getWorkStatus():
    pass

def getUnixtime():
    pass

if __name__ == "__main__":

    videoPath = 'xxx'
    #图片抽取规则每个*帧抽取一张，默认100
    rule_num = 100

    
    cap = cv2.VideoCapture(videoPath)  # 打开视频
    i = 0

    while cap.isOpened():
        ret, fram = cap.read()  # 读取视频返回视频是否结束的bool值和每一帧的图像
        if ret == False:
            break
        if i % rule_num == 0:
            i += 1
            try:
                producer = KafkaProducer(bootstrap_servers=conf['bootstrap_servers'])
                future = producer.send(conf['topic_name']['source'], 'hello kafka2!'.encode())
                future.get()
                log('send message succeed.')
            except KafkaError  as e:
                log('Error:',e)