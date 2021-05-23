from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox
import requests
import json
import os
import sys
import urllib.request

class SearchMovie:
    def __init__(self):
        self.mainWnd = Tk()
        self.mainWnd.geometry("600x400")
        self.mainWnd.title("영화 검색")

        explainL = Label(self.mainWnd, text='영화 제목', font=("Courier",15))
        explainL.place(x=0,y=0)

        self.movieNmEt = Entry(self.mainWnd, bd=5)
        self.movieNmEt.pack()
        self.movieNmEt.place(x=0,y=30, width=100,height=40)

        searchBt = Button(self.mainWnd, font=('Courier',15), text='검색',
                        command=self.search)
        searchBt.pack()
        searchBt.place(x=100,y=30)

        self.mainWnd.mainloop()

    def search(self):
        self.strSearch = self.movieNmEt.get()

        client_id = "tvo5aUWG9rwBq1YRMqyJ"
        client_secret = "40VkT1fuAS"
        header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
        url = f"https://openapi.naver.com/v1/search/movie.json?query={self.strSearch}"
        res=requests.get(url,headers=header_parms)

        self.Alldata = res.json()
        movieCnt = len(self.Alldata['items'])
        self.title = []
        self.link = []
        self.date = []
        self.director = []
        self.actors = []
        self.rating = []

        for i in range(movieCnt):
            self.title.append(self.Alldata['items'][i]['title'].strip('</b>'))
            self.link.append(self.Alldata['items'][i]['link'])
            self.date.append(self.Alldata['items'][i]['pubDate'])
            self.director.append(self.Alldata['items'][i]['director'].split('|')[0])
            self.actors.append(self.Alldata['items'][i]['actor'].split('|')[:-1])
            self.rating.append(float(self.Alldata['items'][i]['userRating']))

        self.showInfo()

    def showInfo(self):
        pass