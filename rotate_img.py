import cv2
import numpy as np
import os


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
    root_dir = './data'
    rotate_angle = 90
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            path = os.path.join(root, file)
            src = cv2.imread(path)
            rotate_img = rotate_bound(src, rotate_angle)
            cv2.imwrite('./data2/'+file, rotate_img)
