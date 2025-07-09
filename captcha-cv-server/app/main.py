# -*- coding: utf-8 -*-
# @Time    : 2025/7/9 17:43
# @Author  : zhaoxiangpeng
# @File    : main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.api.errors.validation_error import request_validation_exception_handler
# 导入顶级api路由
from app.api.routers import api

from app.core.config import settings


def get_application() -> FastAPI:
    if settings.MODEL == 'dev':
        # 开发环境开启文档
        application = FastAPI()
    else:
        application = FastAPI(docs_url=None, redoc_url=None)

    # 加CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 参数异常处理
    application.add_exception_handler(RequestValidationError, request_validation_exception_handler)

    application.include_router(api.router, prefix="/" + settings.SERVICE_NAME)

    return application


app = get_application()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
