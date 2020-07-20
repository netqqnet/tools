import cv2,os
import numpy as np
'''
视频转图片
'''
def rotate_bound(image, angle):
    # 获取图像的尺寸
    # 旋转中心
    (h, w) = image.shape[:2]
    (cx, cy) = (w / 2, h / 2)

    # 设置旋转矩阵
    M = cv2.getRotationMatrix2D((cx, cy), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # 计算图像旋转后的新边界
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # 调整旋转矩阵的移动距离（t_{x}, t_{y}）
    M[0, 2] += (nW / 2) - cx
    M[1, 2] += (nH / 2) - cy
    return cv2.warpAffine(image, M, (nW, nH))

if __name__ == "__main__":
    videoPath = '/Users/linqing/Documents/项目/环卫/数据/more/最原始数据/道路正例/VID_20200707_085001.mp4'

    (filepath,tempfilename) = os.path.split(videoPath)
    (shotname,extension) = os.path.splitext(tempfilename)
    savePicturePath = os.path.join(filepath,shotname)
    if not os.path.exists(savePicturePath):
        os.mkdir(savePicturePath)

    cap = cv2.VideoCapture(videoPath)  # 打开视频
    kl = 0
    eve_num = 50
    ##选择角度
    rotate_angle = 0
    while cap.isOpened():
        ret, fram = cap.read()  # 读取视频返回视频是否结束的bool值和每一帧的图像
        if ret == False:
            break
        else:
            if kl % eve_num == 0 and ret == True:
                path = savePicturePath + '/' + shotname + '-' + str(kl) + '.jpg'
                print(path)
                rotate_img = rotate_bound(fram, rotate_angle)
                cv2.imwrite(path, rotate_img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            kl += 1
    print("success!")



