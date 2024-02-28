import subprocess
import sys
import logging

# # 這是你的套件列表
# required_packages = [
#     'tkinter',
#     # 'speedtest-cli',
#     'ttkthemes',
#     'logging',
#     'socket',
#     'requests',
#     'json',
#     'PIL',
#     'io',
#     'os'
# ]

# for package in required_packages:
#     logging.info(f"嘗試導入套件：{package}")
#     try:
#         # 嘗試導入套件
#         __import__(package)
#     except ImportError:
#         logging.error(f"導入失敗，嘗試安裝套件：{package}")
#         # 如果導入失敗，則安裝套件
#         subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

import tkinter as tk
import tkinter.font
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import speedtest
from tkinter import ttk
from ttkthemes import ThemedTk
from threading import Thread
import socket
import requests
import json
from tooltip import CreateToolTip
from PIL import Image, ImageTk
from io import BytesIO
# from dailysent import update_sentence
from tkinter import messagebox as msg
import os

def is_connected():
    try:
        # 連接到 Google 的主機來檢查網路連接
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

# 檢查網路連接
if not is_connected():
    msg.showerror("錯誤", "無法連接到網路，請檢查你的網路設置。")
    sys.exit()

class CustomFormatter(logging.Formatter):
    """自定義的 Formatter，用於修改 levelname 的輸出內容。"""

    def format(self, record):
        # 修改 levelname 的輸出內容
        if record.levelname == 'DEBUG':
            record.levelname = 'DEBG'
        elif record.levelname == 'WARNING':
            record.levelname = 'WARN'
        elif record.levelname == 'ERROR':
            record.levelname = 'EROR'

        # 調用父類的 format 方法來完成日誌訊息的格式化
        return super().format(record)

# 創建一個 logger
logger = logging.getLogger(__name__)

# 創建一個 handler
handler = logging.StreamHandler()

# 創建一個自定義的 Formatter
formatter = CustomFormatter('%(asctime)s [%(levelname)s] : %(message)s')

# 將自定義的 Formatter 設定給 handler
handler.setFormatter(formatter)

# 將 handler 添加到 logger
logger.addHandler(handler)

# 設定 logger 的等級
logger.setLevel(logging.DEBUG)

# 設定 matplotlib 的 logger 的等級
mpl_logger = logging.getLogger('matplotlib')
mpl_logger.setLevel(logging.DEBUG)

# 設定 speedtest 的 logger 的等級
speedtest_logger = logging.getLogger('speedtest')
speedtest_logger.setLevel(logging.DEBUG)

# 設定 requests 的 logger 的等級
requests_logger = logging.getLogger('requests')
requests_logger.setLevel(logging.DEBUG)

# 設定 ttkthemes 的 logger 的等級
ttkthemes_logger = logging.getLogger('ttkthemes')
ttkthemes_logger.setLevel(logging.DEBUG)

# 設定 tkinter 的 logger 的等級
tkinter_logger = logging.getLogger('tkinter')
tkinter_logger.setLevel(logging.DEBUG)

def run_speedtest():
    progress_bar.start(5)  # 開始進度條動畫
    run_button.config(state="disabled")  # 禁用按鈕
    logging.info("開始測速")

    def speedtest_thread():
        # 如果被403錯誤則直接中斷
        try:
            logging.info("目前進度：連接 > 嘗試連接至 Speedtest.net 伺服器")
            st = speedtest.Speedtest()
            logging.info("目前進度：連接 > 成功連接至 Speedtest.net 伺服器")
        except speedtest.ConfigRetrievalError as e:
            logging.error(f"測速崩潰：連接 > 發生錯誤：{e}")
            progress_bar.stop()  # 停止進度條動畫
            return
        except speedtest.SpeedtestException as e:
            logging.error(f"測速崩潰：連接 > 發生錯誤：{e}")
            progress_bar.stop()
            return

        logging.info("目前進度：下載 > 開始測試下載速度")
        download_speed = st.download() / 10**6  # 將下載速度轉換為兆字節
        logging.info("目前進度：上傳 > 開始測試上傳速度")
        upload_speed = st.upload() / 10**6  # 將上傳速度轉換為兆字節
        logging.info("目前進度：Ping > 開始測試 Ping 值")
        ping = st.results.ping
        # logging.info("目前進度：Ping > 開始測試抖動")
        # jitter = st.results.jitter
        
        # 取得廣域網 IP
        try:
            response = requests.get('https://httpbin.org/ip')
            external_ip = response.json()['origin']
        except Exception as e:
            logging.error(f"測速崩潰：獲取廣域網IP錯誤 > 發生錯誤：{e}")
            external_ip = "未知廣域網 IP"

        # 取得局域網 IP
        try:
            # 獲取內網 IP 地址
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            internal_ip = s.getsockname()[0]
            s.close()
        except Exception as e:
            logging.error(f"測速崩潰：獲取局域網IP錯誤 > 發生錯誤：{e}")
            internal_ip = "未知局域網 IP"

        # 更新標籤文本
        logging.info("目前進度：更新標籤文本")
        download_label.config(text=f"{download_speed:.2f} Mbps")
        upload_label.config(text=f"{upload_speed:.2f} Mbps")
        ping_label.config(text=f"{ping:.2f} ms")
        # jitter_label.config(text=f"{jitter:.2f} ms")
        # isp_name_label.config(text=isp_name)
        local_ip_label.config(text=internal_ip)
        public_ip_label.config(text=external_ip)

        # 換算單位
        change_unit()

        logging.info("目前進度：終止進度條動畫")
        progress_bar.stop()  # 停止進度條動畫
        logging.info("測速完成")
        run_button.config(state="normal")

    # 在新的線程中執行測速
    thread = Thread(target=speedtest_thread)
    thread.start()

# 創建主窗口
root = ThemedTk(theme="arc")
root.title("Speedtest GUI")
root.geometry("400x700")
root.resizable(False, False)

# 獲取 ttk 風格的預設背景顏色
style = ttk.Style()
default_bg = style.lookup("TFrame", "background")

# 將視窗的背景顏色設定為預設背景顏色
root.configure(bg=default_bg)

# 創建表格
# root = ttk.root(root)
# root.pack()

# 創建標籤

"""
主題：
        0        1
0| 下載速度標籤 | Ping值標籤 |
1| Download Speed 文字標籤 | Ping 文字標籤 |
2| 上傳速度標籤 | 抖動標籤 |
3| Upload Speed 文字標籤 | 抖動 文字標籤 |
4| 空格子 | 測速按鈕 |
5| 輸出折線圖(跨兩行) | 輸出折線圖(跨兩行) |
"""

# 先檢查是否有安裝 Noto Sans TC 思源黑體字型，否則使用微軟正黑體
font_list = list(tk.font.families())
if "Noto Sans TC" in font_list:
    logger.debug("使用 Noto Sans TC 思源黑體字型")
    # 使用 Noto Sans TC 思源黑體字型，並設定粗細為 400em
    normal_font_style = ("Noto Sans TC", 12, "normal")
    bold_font_style = ("Noto Sans TC", 24, "bold")
else:
    logger.debug("未安裝 Noto Sans TC 思源黑體字型，使用微軟正黑體")
    normal_font_style = ("微軟正黑體", 12, "normal")
    bold_font_style = ("微軟正黑體", 24, "bold")

# # 創建一個 Frame 作為每日一句容器
# container = ttk.Label(root)
# container.grid(row=0, column=0, sticky='ew')

# # 讓容器在水平方向上擴展以填充窗口
# root.grid_columnconfigure(0, weight=1)

# # 在容器中添加一個 Label 來顯示每日一句
# daily_sentence = ttk.Label(container, text="學如逆水行舟，不進則退。", background=transparent, font=normal_font_style, wraplength=300, justify="center")
# daily_sentence.pack(fill='x')

# 換算函式
def change_unit(event=None, x=None, y=None):
    logging.info(f"目前狀態：換算網速")
    logging.info(f"  > 網速單位：{unit_var.get()}")
    if unit_var.get() == old_var:
        logging.warning("  > 網速單位未更改")
        return
    
    current_unit = download_label.cget('text').split()[1]
    target_unit = unit_var.get()

    if current_unit == target_unit:
        return

    speed = float(download_label.cget('text').split()[0])

    if current_unit == "Mbps":
        if target_unit == "Mb/s":
            speed *= 8
        elif target_unit == "Kbps":
            speed *= 1000
        elif target_unit == "Kb/s":
            speed *= 8000
    elif current_unit == "Mb/s":
        if target_unit == "Mbps":
            speed /= 8
        elif target_unit == "Kbps":
            speed *= 125
        elif target_unit == "Kb/s":
            speed *= 1000
    elif current_unit == "Kbps":
        if target_unit == "Mbps":
            speed /= 1000
        elif target_unit == "Mb/s":
            speed /= 125
        elif target_unit == "Kb/s":
            speed /= 8
    elif current_unit == "Kb/s":
        if target_unit == "Mbps":
            speed /= 8000
        elif target_unit == "Mb/s":
            speed /= 1000
        elif target_unit == "Kbps":
            speed *= 8

    download_label.config(text=f"{speed:.2f} {target_unit}")
    upload_label.config(text=f"{speed:.2f} {target_unit}")

# 在 Mbps 與 Mb/s 更換網速單位的下拉選單
unit_list = ["Mbps", "Mb/s", "Kbps", "Kb/s"]
unit_var = tk.StringVar()
old_var = unit_var.get()
# 計算 unit_list 中最長的項目的長度
max_length = max(len(item) for item in unit_list)
# 創建 Combobox，並將其寬度設定為 max_length
unit_menu = ttk.Combobox(root, textvariable=unit_var, values=unit_list, width=max_length, style='TButton')
unit_menu.grid(row=12, column=0, pady=10, sticky="ew")
unit_var.trace_add("write", change_unit)

# 創建一個新的風格
btnStyle = ttk.Style()
btnStyle.configure('TButton', font=normal_font_style)

# 創建粗體風格，繼承 TButton 風格
btnStyle.configure('Bold.TButton', font=bold_font_style + ("bold",))
# 套用方式：style='Bold.TButton'

download_label = ttk.Label(root, text="0.00 Mbps", font=bold_font_style)
download_label.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
download_label_tooltip = CreateToolTip(download_label, f"下載速度 (Download Speed)，即為從伺服器下載數據的速度，目前選取單位為{unit_var.get()}。\n\n下載速度越快，則下載文件的速度越快，例如下載遊戲、電影、音樂等文件的速度。通常下載速度會比上傳速度快很多。例如，如果下載速度為 100 Mbps，則下載 1 GB 的文件只需要 80 秒。")

download_text_label = ttk.Label(root, text="↓ 下載速度", font=normal_font_style)
download_text_label.grid(row=2, column=0, sticky="ew", padx=10, pady=5)

upload_label = ttk.Label(root, text="0.00 Mbps", font=bold_font_style)
upload_label.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
upload_label_tooltip = CreateToolTip(upload_label, f"上傳速度 (Upload Speed)，即為上傳數據到伺服器的速度，目前選取單位為{unit_var.get()}。\n\n上傳速度越快，則上傳文件的速度越快，例如上傳文件到雲端硬碟、發送郵件附件等。通常上傳速度會比下載速度慢很多。例如，如果上傳速度為 10 Mbps，則上傳 1 GB 的文件需要 13 分鐘。")

upload_text_label = ttk.Label(root, text="↑ 上傳速度", font=normal_font_style)
upload_text_label.grid(row=4, column=0, sticky="ew", padx=10, pady=5)

ping_label = ttk.Label(root, text="0 ms", font=bold_font_style)
ping_label.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
ping_label_tooltip = CreateToolTip(ping_label, "Ping 值，即為測試數據包從您的設備發送到伺服器並返回的時間，通常以毫秒為單位。\n\nPing 值越小，則網絡連接速度越快，例如在遊戲中的延遲時間越短。")

ping_text_label = ttk.Label(root, text="Ping值", font=normal_font_style)
ping_text_label.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

# jitter_label = ttk.Label(root, text="0 ms", font=bold_font_style)
# jitter_label.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
# jitter_label_tooltip = CreateToolTip(jitter_label, "抖動 (Jitter)，即為 Ping 值的變化量，通常以毫秒為單位。\n\n抖動越小，則網絡連接速度越穩定，例如在遊戲中的延遲時間變化越小。")

# jitter_text_label = ttk.Label(root, text="抖動", font=normal_font_style)
# jitter_text_label.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

# 因為當前版本不支持此功能，所以將其設定為灰色
isp_name_label = ttk.Label(root, text="不支持此功能", font=bold_font_style, foreground="gray")
isp_name_label.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10, pady=5)
isp_name_label_tooltip = CreateToolTip(isp_name_label, "運營商 (ISP)，即為您當前所使用的網絡服務提供商的名稱。\n\n因為實現此項目之偵測需要設定 API 金鑰，較為麻煩，所以當前版本不支持此功能。")

isp_name_text_label = ttk.Label(root, text="運營商 (ISP)", font=normal_font_style)
isp_name_text_label.grid(row=4, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

local_ip_label = ttk.Label(root, text="未知局域網 IP", font=bold_font_style)
local_ip_label.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
local_ip_label_tooltip = CreateToolTip(local_ip_label, "局域網 IP，又稱內網 IP 或私有 IP，即為您當前所連接的網絡的 IP 地址。\n\n例如，如果您連接的是家用 Wi-Fi 網絡，則局域網 IP 可能為 192.168.x.x 的格式。")

local_ip_text_label = ttk.Label(root, text="局域網 IP", font=normal_font_style)
local_ip_text_label.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

public_ip_label = ttk.Label(root, text="未知廣域網 IP", font=bold_font_style)
public_ip_label.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
public_ip_label_tooltip = CreateToolTip(public_ip_label, "廣域網 IP，又稱外網 IP 或公有 IP，即為您當前所連接的網絡的 IP 地址。\n\n例如，如果您連接的是家用 Wi-Fi 網絡，則廣域網 IP 可能為 114.36.x.x 的格式。")

public_ip_text_label = ttk.Label(root, text="廣域網 IP", font=normal_font_style)
public_ip_text_label.grid(row=8, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

# 創建進度條
progress_bar = ttk.Progressbar(root, mode='indeterminate', length=200, orient="horizontal")
progress_bar.grid(row=9, column=0, columnspan=2, pady=10)

# 創建按鈕
run_button = ttk.Button(root, text="Run Speedtest", command=run_speedtest, style='TButton')
run_button.grid(row=12, column=1, pady=10)
run_button_tooltip = CreateToolTip(run_button, "點擊此按鈕以開始測速。")

# update_sentence(daily_sentence=daily_sentence, container=container)

# 執行主迴圈
root.mainloop()