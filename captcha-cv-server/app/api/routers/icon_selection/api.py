# -*- coding: utf-8 -*-
# @Time    : 2025/7/10 9:34
# @Author  : zhaoxiangpeng
# @File    : api.py

from fastapi import APIRouter

from .chaoxing import ChaoxingIconSelection


router = APIRouter(prefix='/iconSelection')

router.include_router(ChaoxingIconSelection().router)
