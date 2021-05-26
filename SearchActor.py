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

class SearchActor:
    def __init__(self):
        self.mainWnd = Tk()
        self.mainWnd.geometry("600x450")
        self.mainWnd.title("배우 검색")
        self.movieCnt = 0

        self.movieNmEt = Entry(self.mainWnd, bd=5)
        self.movieNmEt.pack()
        self.movieNmEt.place(x=110,y=30, width=100,height=40)

        # 정보 보기 버튼
        self.infoBt = Button(self.mainWnd, font=('Courier',15), text='정보보기',
                         command=self.showInfo)
        self.infoBt.place(x=290,y=30)

    def showInfo(self):
        dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=edfd0508a0320efa8abbe1eeba097a94&peopleNm="
        dayOfficeURL += self.movieNmEt.get()
        res = requests.get(dayOfficeURL)
        text = res.text
        d = json.loads(text)
        for b in d['peopleListResult']['peopleList']:
            print(b)
        pass