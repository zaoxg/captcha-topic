# -*- coding: utf-8 -*-
# @Time    : 2025/2/28 10:54
# @Author  : zhaoxiangpeng
# @File    : config.py
# app/core/config.py

import os
from pydantic import BaseConfig

fast_api_env = os.environ.get('FAST_API_ENV')


class Development(BaseConfig):
    MODEL = 'dev'

    SERVICE_NAME = 'fastapi_captcha_service'

    class Config:
        env_file = ".env"


class Product(BaseConfig):
    MODEL = 'pro'

    SERVICE_NAME = 'fastapi_captcha_service'

    class Config:
        env_file = ".env"


print('当前运行环境: %s' % fast_api_env)
settings = Development() if fast_api_env != 'dev' else Product()

