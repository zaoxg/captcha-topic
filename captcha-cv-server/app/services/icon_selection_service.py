# -*- coding: utf-8 -*-
# @Time    : 2025/7/10 10:35
# @Author  : zhaoxiangpeng
# @File    : icon_selection_service.py

import random
import numpy as np
import cv2
import torch
from .third_party.yidun import get_cut_img, parse_y_pred

from app.core.model_manager import model_manager, DEVICE


def get_clz_rect(npimg, state):

    net = state['net']
    anchors = state['anchors']
    class_types = state['class_types']

    height, width = npimg.shape[:2]
    npimg = cv2.cvtColor(npimg, cv2.COLOR_BGR2RGB)  # [y,x,c]
    npimg = cv2.resize(npimg, (416, 416))
    npimg_ = np.transpose(npimg, (2, 1, 0))  # [c,x,y]
    y_pred = net(torch.FloatTensor(npimg_).unsqueeze(0).to(DEVICE))
    v = parse_y_pred(y_pred, anchors, class_types, islist=True, threshold=0.2, nms_threshold=0.4)
    ret = []
    for i in v:
        rect, clz, con, log_cons = i
        rw, rh = width / 416, height / 416
        rect[0], rect[2] = int(rect[0] * rw), int(rect[2] * rw)
        rect[1], rect[3] = int(rect[1] * rh), int(rect[3] * rh)
        ret.append([clz, rect])
    return ret


def icon_selection_detection(contents: bytes):
    np_arr = np.frombuffer(contents, np.uint8)
    img = s = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    # 从图中拿出小图标
    a = s[160:, 0 * 28:1 * 28 - 6, :]
    b = s[160:, 1 * 28:2 * 28 - 6, :]
    c = s[160:, 2 * 28:3 * 28 - 6, :]
    a1, a2 = a[40:60], a[0:20]
    b1, b2 = b[40:60], b[0:20]
    c1, c2 = c[40:60], c[0:20]

    def get_match_lens(i1, i2):
        i1 = cv2.resize(i1, (int(i1.shape[1] * 8), int(i1.shape[0] * 8)))
        i2 = cv2.resize(i2, (i2.shape[1] * 4, i2.shape[0] * 4))
        s = cv2.SIFT.create()
        kp1, des1 = s.detectAndCompute(i1, None)
        kp2, des2 = s.detectAndCompute(i2, None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        DIS = .88
        for m, n in matches:
            if m.distance <= DIS * n.distance:
                good.append([m])
        i3 = cv2.drawMatchesKnn(i1, kp1, i2, kp2, good, None)
        # cv2.imshow('nier', i3)
        # cv2.waitKey(0)
        return len(good)

    def get_flag_rect(k12, cut_imgs, st):
        k1, k2 = k12
        r = []
        for clz, npimg, rect in cut_imgs:
            if clz == '1':
                r1 = get_match_lens(k1, npimg)
                r.append([r1, rect, st])
            if clz == '2':
                r2 = get_match_lens(k2, npimg)
                r.append([r2, rect, st])
        return sorted(r, key=lambda i: i[0])

    state = model_manager.get_state("yidun")
    v = get_cut_img(s, get_clz_rect(img, state))
    rs1 = get_flag_rect([a1, a2], v, 1)
    rs2 = get_flag_rect([b1, b2], v, 2)
    rs3 = get_flag_rect([c1, c2], v, 3)
    rs = rs1 + rs2 + rs3
    r = []
    t = []
    v = max([j for j in rs if j[2] not in t], key=lambda i: i[0])
    r.append(v)
    t.append(v[2])
    q = []
    for i in rs:
        if i[1] == v[1]:
            q.append(i)
    for i in q:
        rs.remove(i)
    v = max([j for j in rs if j[2] not in t], key=lambda i: i[0])
    r.append(v)
    t.append(v[2])
    q = []
    for i in rs:
        if i[1] == v[1]:
            q.append(i)
    for i in q:
        rs.remove(i)
    v = max([j for j in rs if j[2] not in t], key=lambda i: i[0])
    r.append(v)
    t.append(v[2])
    r1, r2, r3 = sorted(r, key=lambda i: i[2])
    return r1[1], r2[1], r3[1]


def get_xy_location(rect: tuple):
    """
    在矩形框内随机选点
    :param rect: 矩形框的左上、右下坐标点
    :return:
    """
    offset = 10
    l1 = rect[:2]  # 左上坐标
    l2 = rect[2:]  # 右下坐标

    x_offset = random.randint(offset, (l2[0] - l1[0]) - offset)
    y_offset = random.randint(offset, (l2[1] - l1[1]) - offset)
    return dict(
        x=l1[0]+x_offset,
        y=l1[1]+y_offset
    )
