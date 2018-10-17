# coding:utf-8
"""
    try to implement welsh's paper: Transferring Color to Greyscale Images
"""
import cv2
import argparse
import random
import numpy as np
from scipy import signal

"""
    图像尺寸变成1024*1024
    @return 256 个示例点
"""


def jitter_sampling(img):
    num_samples = 256
    samples_in_a_row = 16
    block_size = 1024 / 16
    jitter_samples = [
        ((j * block_size) + (random.randint(0, block_size - 1)),
         (i * block_size) + (random.randint(0, block_size - 1)))
        for i in range(samples_in_a_row) for j in range(samples_in_a_row)]
    return jitter_samples


def neighbour_standard_dev(img: np.ndarray):
    if img.shape[2] == 3:
        # channels = cv2.split(img)
        # luminance = channels[0]
        # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
        luminance = img[:, :, 0]
    elif img.shape[2] == 1:
        luminance = img[:, :, :]
    else:
        raise RuntimeError("Only available for 1 and 3 channel images")
    r = 2
    luminance = cv2.copyMakeBorder(luminance, r, r, r, r, cv2.BORDER_CONSTANT, value=0)
    result = np.zeros(img.shape)
    luminance_rows, luminance_cols = luminance.shape
    # 使用卷积加速计算
    mean = signal.convolve2d(luminance, np.ones((5, 5)) / 25, boundary='symm', mode='same')
    for i in range(r, luminance_rows - r):
        for j in range(r, luminance_cols - r):
            sdev = np.sum(np.sum(np.power(luminance[i - r:i + r + 1, j - r:j + r + 1] - mean[i, j], 2))) / 25
            result[i - r, j - r] = sdev
    result = np.power(result, 0.5)
    return result


def colorize(reference, grey):
    jitter_samples = jitter_sampling(reference)
    reference_sdev = neighbour_standard_dev(reference)
    grey_sdev = neighbour_standard_dev(grey)

    sample_values = [
        reference[jitter_samples[i][0], jitter_samples[i][1]][0] + reference_sdev[
            jitter_samples[i][0], jitter_samples[i][1]]
        for i in range(jitter_samples.__len__())
    ]
    result = np.zeros(grey.shape)
    for i in range(grey.shape[0]):
        for j in range(grey.shape[1]):
            value = grey[i, j] + grey_sdev[i, j]
            # 找到最接近的一个
            min_index, _ = min(enumerate(map(lambda x: abs(value - x), sample_values)),
                               key=lambda x: x[1])
            x, y = jitter_samples[min_index]
            hue = reference[x, y][1]
            sat = reference[x, y][2]
            result[i, j] = grey[i, j], hue, sat
    return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('template_colored_image', type=str)
    parser.add_argument('grey_image', type=str)
    parser.add_argument('-o', dest='output_image', default='output.jpg', type=str)
    args = parser.parse_args()

    ref = cv2.imread(args.template_colored_image)
    ref = cv2.resize(ref, (1024, 1024))
    ref_lab = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB)

    grey = cv2.imread(args.grey_image)
    colorize(ref_lab, grey)
    # cv2.imwrite('output.jpg',colorize(ref_lab,grey))
