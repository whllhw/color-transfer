# -*- coding: utf-8 -*-
"""
    implement reinhard's paper: Color Transfer between Images
"""
import cv2
import numpy as np

image = cv2.imread('src.jpg')
# 转化颜色空间到 LAB 空间
image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
original = cv2.imread('ref.jpg')
original = cv2.cvtColor(original, cv2.COLOR_BGR2LAB)


def get_avg_std(image):
    """
        @return 图片的均值和标准差
    """
    avg = []
    std = []
    image_avg_l = np.mean(image[:, :, 0])
    image_std_l = np.std(image[:, :, 0])
    image_avg_a = np.mean(image[:, :, 1])
    image_std_a = np.std(image[:, :, 1])
    image_avg_b = np.mean(image[:, :, 2])
    image_std_b = np.std(image[:, :, 2])
    avg.append(image_avg_l)
    avg.append(image_avg_a)
    avg.append(image_avg_b)
    std.append(image_std_l)
    std.append(image_std_a)
    std.append(image_std_b)
    print(avg)
    print(std)
    return avg, std


image_avg, image_std = get_avg_std(image)
original_avg, original_std = get_avg_std(original)
# 每个通道进行如下操作
# 减去原图像平均值乘以目标图像标准差与原图像标准差的比值加上目标图像的均值
height, width, channel = image.shape
for i in range(0, height):
    for j in range(0, width):
        for k in range(0, channel):
            t = image[i, j, k]
            t = (t - image_avg[k]) * (original_std[k] / image_std[k]) + original_avg[k]
            t = 0 if t < 0 else t
            t = 255 if t > 255 else t
            image[i, j, k] = t

image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
cv2.imwrite('out.jpg', image)
