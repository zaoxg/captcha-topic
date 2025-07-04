# -*- coding: utf-8 -*-
# @Time    : 2025/6/13 9:11
# @Author  : zhaoxiangpeng
# @File    : cv.py

import cv2
import numpy as np

# 加载图像
img = cv2.imread("H:/captcha/5FCD9C8D2EB337E89D3579CA52696782.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('g', gray)

# 分离图像上半部分（搜索区域）和下半部分（模板区域）
h, w = gray.shape
search_area = gray[:int(h//1.5), :]
template_area = gray[int(h//1.5):int(h//1.5)+20, :int(w//4)]
# cv2.imshow('template', template_area)

# 模板网格划分参数（3x3）
rows, cols = 1, 3
th = template_area.shape[0] // rows  # 模板高度
tw = template_area.shape[1] // cols  # 模板宽度

# 匹配阈值（调整此值控制灵敏度）
threshold = 0.7
# 图标缩放比例
scaling = 0.5


# 二值化
_, template_bin = cv2.threshold(template_area, 128, 255, cv2.THRESH_BINARY_INV)
_, search_bin = cv2.threshold(search_area, 128, 255, cv2.THRESH_BINARY_INV)

# 1. 提取模板图标轮廓
contours_template, _ = cv2.findContours(template_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 2. 提取搜索区域轮廓
contours_search, _ = cv2.findContours(search_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 3. 匹配轮廓
result_img = img.copy()
for idx_temp, cnt_temp in enumerate(contours_template):
    if cv2.contourArea(cnt_temp) < 20:  # 忽略太小的噪声
        print('忽略太小的噪声')
        continue

    for cnt_search in contours_search:
        if cv2.contourArea(cnt_search) < 100:
            continue

        # 计算形状相似度
        score = cv2.matchShapes(cnt_temp, cnt_search, cv2.CONTOURS_MATCH_I1, 0.0)
        if score < 0.15:  # 形状越相似，得分越低
            # 高匹配，画出轮廓
            cv2.drawContours(result_img, [cnt_search], -1, (0, 255, 0), 2)

# 显示或保存结果
cv2.imshow("Feature Matching (Scale & Rotation)", result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

