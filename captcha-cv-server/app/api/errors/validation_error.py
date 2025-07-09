# -*- coding: utf-8 -*-
# @Time    : 2022/11/15 14:28
# @Author  : ZAOXG
# @File    : validation_error.py

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status


async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError) -> JSONResponse:
    print(f"参数不对{request.method} {request.url}")
    return JSONResponse({
        "code": 400,
        "msg": exc.errors()
    }, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
