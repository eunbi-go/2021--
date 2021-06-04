from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox
import requests
import json
import os
import sys
import urllib
import urllib.request
from io import BytesIO
from PIL import Image,ImageTk
import webbrowser
from bs4 import BeautifulSoup

url = "https://openapi.gg.go.kr/MovieTheater?SIGUN_NM="
url += '시흥시'

res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
data = soup.find_all('row')

for item in data:
    nm = item.find('bizplc_nm')
    print(nm)