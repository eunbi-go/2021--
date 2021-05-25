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
        self.movieCnt = 0

        explainL = Label(self.mainWnd, text='영화 제목', font=("Courier",15))
        explainL.place(x=0,y=0)

        self.movieNmEt = Entry(self.mainWnd, bd=5)
        self.movieNmEt.pack()
        self.movieNmEt.place(x=0,y=30, width=100,height=40)

        searchBt = Button(self.mainWnd, font=('Courier',15), text='검색',
                        command=self.search)
        searchBt.pack()
        searchBt.place(x=100,y=30)

        # 영화 정보 표기
        self.movieListbox = Listbox(self.mainWnd, width=25,height=18, relief='solid')
        self.movieListbox.pack()
        self.movieListbox.place(x=0,y=90)

        # 개봉일
        dateL = Label(self.mainWnd, text='개봉일', font=("Courier",15))
        dateL.place(x=200,y=100)

        # 감독
        directorL = Label(self.mainWnd, text='감독', font=("Courier",15))
        directorL.place(x=200,y=150)

        # 출연 배우
        actorsL = Label(self.mainWnd, text='출연배우', font=("Courier",15))
        actorsL.place(x=200,y=200)

        # 평점
        ratingL = Label(self.mainWnd, text='평점', font=("Courier",15))
        ratingL.place(x=200,y=250)

        # 개봉일
        self.labelDate = Label(self.mainWnd, font=("Courier",15), text=' ')
        self.labelDate.pack()
        self.labelDate.place(x=300,y=100)
        # 감독
        self.labelDirector = Label(self.mainWnd, font=("Courier",15), text=' ')
        self.labelDirector.pack()
        self.labelDirector.place(x=300,y=150)
        # 출연배우
        self.labelActors = Label(self.mainWnd, font=("Courier",15), text=' ')
        self.labelActors.pack()
        self.labelActors.place(x=300,y=200)
        # 평점
        self.labelRate = Label(self.mainWnd, font=("Courier",15), text=' ')
        self.labelRate.pack()
        self.labelRate.place(x=300,y=250)

        # 정보 보기 버튼
        self.infoBt = Button(self.mainWnd, text='정보보기', command=self.showInfo)
        self.infoBt.place(x=400,y=100)

        self.mainWnd.mainloop()

    def search(self):
        self.strSearch = self.movieNmEt.get()

        client_id = "tvo5aUWG9rwBq1YRMqyJ"
        client_secret = "40VkT1fuAS"
        header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
        url = f"https://openapi.naver.com/v1/search/movie.json?query={self.strSearch}"
        res=requests.get(url,headers=header_parms)

        self.Alldata = res.json()
        self.movieCnt = len(self.Alldata['items'])
        self.title = []
        self.link = []
        self.date = []
        self.director = []
        self.actors = []
        self.rating = []

        for i in range(self.movieCnt):
            self.title.append(self.Alldata['items'][i]['title'].strip('</b>').replace('<b>','').replace('</b>',''))
            self.link.append(self.Alldata['items'][i]['link'])
            self.date.append(self.Alldata['items'][i]['pubDate'])
            self.director.append(self.Alldata['items'][i]['director'].split('|')[0])
            self.actors.append(self.Alldata['items'][i]['actor'].split('|')[:-1])
            self.rating.append(float(self.Alldata['items'][i]['userRating']))

        self.showTitle()

    def showTitle(self):
        for i in range(self.movieCnt):
            self.movieListbox.insert(i, self.title[i])

    def showInfo(self):
        self.indexInfo = self.movieListbox.curselection()[0]
        self.labelDate.config(text=self.date[self.indexInfo])
        self.labelDirector.config(text=self.director[self.indexInfo])
        self.labelActors.config(text=self.actors[self.indexInfo])
        self.labelRate.config(text=self.rating[self.indexInfo])
