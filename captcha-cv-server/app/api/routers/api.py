# -*- coding: utf-8 -*-
# @Time    : 2025/7/9 17:49
# @Author  : zhaoxiangpeng
# @File    : api.py

from fastapi import APIRouter

from .icon_selection import api as icon_selection

router = APIRouter()

router.include_router(icon_selection.router)
