# -*- coding: utf-8 -*-
# @Time    : 2025/7/9 17:55
# @Author  : zhaoxiangpeng
# @File    : chaoxing.py

from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse

from app.services.icon_selection_service import icon_selection_detection, get_xy_location


class ChaoxingIconSelection:
    def __init__(self):
        self.router = APIRouter(prefix='/chaoxing')
        self.router.add_api_route('/', endpoint=self.test_page, methods=['GET'])
        self.router.add_api_route('/uploadImg', endpoint=self.upload_img, methods=['POST'])
        self.router.add_api_route('/uploadUrl', endpoint=self.upload_url, methods=['POST'])

    async def test_page(self):
        content = """
        <body>
        <form action="/fastapi_captcha_service/iconSelection/chaoxing/uploadImg" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        <form action="/fastapi_captcha_service/iconSelection/chaoxing/uploadImg" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
        </form>
        </body>
            """
        return HTMLResponse(content=content)

    async def upload_img(self, file: UploadFile = File(...)):
        # 读取图片数据
        image_data = await file.read()
        rects = icon_selection_detection(image_data)
        points = {}
        i = 0
        for rect in rects:
            point = get_xy_location(rect)
            points.setdefault(i := i+1, point)
        return {"filename": file.filename, "content_type": file.content_type, "rects": [list(r) for r in rects], "random_points": points}

    async def upload_url(self):
        pass
