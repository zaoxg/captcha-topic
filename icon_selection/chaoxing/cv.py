# -*- coding: utf-8 -*-
# @Time    : 2025/6/13 9:11
# @Author  : zhaoxiangpeng
# @File    : cv.py

import cv2
import numpy as np

# 打开图像
img = cv2.imread(r"C:\Users\zzz\Desktop\5FCD9C8D2EB337E89D3579CA52696782.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 分离搜索区域与模板区域
h, w = gray.shape
search_area = gray[:h//2, :]
template_area = gray[h//2:, :]

# 上传 search_area 到 GPU
gpu_search = cv2.cuda.GpuMat()
gpu_search.upload(search_area)

# 模板配置
rows, cols = 3, 3  # 模板网格布局
th, tw = template_area.shape[0] // rows, template_area.shape[1] // cols

# 匹配阈值
threshold = 0.75

# 结果图像（复制原图）
result_img = img.copy()

# 遍历每个模板
for i in range(rows):
    for j in range(cols):
        # 裁切模板
        template = template_area[i*th:(i+1)*th, j*tw:(j+1)*tw]

        # 上传模板到 GPU
        gpu_template = cv2.cuda.GpuMat()
        gpu_template.upload(template)

        # 模板匹配
        gpu_result = cv2.matchTemplate(gpu_search, gpu_template, cv2.TM_CCOEFF_NORMED)
        result = gpu_result.download()

        # 获取匹配位置
        loc = np.where(result >= threshold)

        # 在原图上标注匹配框
        for pt in zip(*loc[::-1]):
            top_left = (pt[0], pt[1])
            bottom_right = (pt[0] + tw, pt[1] + th)
            cv2.rectangle(result_img, top_left, bottom_right, (0, 255, 0), 2)

# 显示或保存结果
cv2.imshow("Detected Icons", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

