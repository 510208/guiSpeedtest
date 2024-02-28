import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from opencc import OpenCC

def update_sentence(daily_sentence: ttk.Label, container: ttk.Label):
    # 發起 GET 請求
    response = requests.get("http://v3.wufazhuce.com:8000/api/channel/one/0/0")
    data = response.json()

    # 取得每日一句的內容並轉成繁體字
    cc = OpenCC('s2tw')
    forward = cc.convert(data['data']['content_list'][0]['forward'])

    # 更新每日一句的內容
    daily_sentence.config(text=forward)

    # 取得圖片的連結並下載圖片
    image_url = data['data']['content_list'][0]['img_url']
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    photo = ImageTk.PhotoImage(image)

    # 更新容器的背景圖片
    container.config(image=photo)
    container.image = photo  # 保持對圖片的引用