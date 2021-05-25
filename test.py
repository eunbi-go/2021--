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

dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=edfd0508a0320efa8abbe1eeba097a94&movieNm=귀멸의칼날"
res = requests.get(dayOfficeURL)
text = res.text
d = json.loads(text)
code = []
for b in d['movieListResult']['movieList']:
    print(b['movieNm'])
print(len(d['movieListResult']['movieList']))