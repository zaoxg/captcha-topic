# -*- coding: utf-8 -*-
# @Time    : 2025/7/10 10:23
# @Author  : zhaoxiangpeng
# @File    : test_file_upload.py

import requests

# FastAPI服务地址
url = "http://localhost:8000/fastapi_captcha_service/iconSelection/chaoxing/uploadImg"

# 要上传的文件路径
file_path = r"E:\zgit\captcha-topic\captcha-cv-server\app\services\third_party\testimg2\272D8B99BA93EE512AC036F0C244328D.jpg"  # 替换为你的测试图片路径

# 发送POST请求
with open(file_path, 'rb') as f:
    files = {'file': (file_path, f, 'image/jpeg')}
    response = requests.post(url, files=files)

print("状态码:", response.status_code)
print("响应内容:", response.json())
