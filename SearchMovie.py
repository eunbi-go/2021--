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



class SearchMovie:
    def __init__(self):
        global frame2
        self.mainWnd = frame2
        self.movieCnt = 0

        self.mainWnd.mainloop()

    def search(self):
        global movieNmEt
        global movieListbox
        self.strSearch = movieNmEt.get()
        movieListbox.delete(0, END)

        # 네이버 openAPI 읽어오기
        client_id = "tvo5aUWG9rwBq1YRMqyJ"
        client_secret = "40VkT1fuAS"
        header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
        url = f"https://openapi.naver.com/v1/search/movie.json?query={self.strSearch}"
        res=requests.get(url,headers=header_parms)

        self.Alldata = res.json()
        self.movieCnt = len(self.Alldata['items'])
        self.title = []
        self.naverlink = []
        self.image = []
        self.date = []
        self.director = []
        self.actors = []
        self.rating = []

        for i in range(self.movieCnt):
            self.title.append(self.Alldata['items'][i]['title'].strip('</b>').replace('<b>','').replace('</b>',''))
            self.naverlink.append(self.Alldata['items'][i]['link'])
            self.image.append(self.Alldata['items'][i]['image'])
            self.date.append(self.Alldata['items'][i]['pubDate'])
            self.director.append(self.Alldata['items'][i]['director'].split('|')[0])
            self.actors.append(self.Alldata['items'][i]['actor'].replace('|', ', '))
            self.rating.append(float(self.Alldata['items'][i]['userRating']))
        self.showTitle()

    def showTitle(self):
        for i in range(self.movieCnt):
            movieListbox.insert(i, self.title[i])

    def showInfo(self):
        global labelDate
        global directorL
        global actorsL
        global labelRate
        self.indexInfo = movieListbox.curselection()[0]
        labelDate.config(text=self.date[self.indexInfo])
        directorL.config(text=self.director[self.indexInfo])
        strLen = len(self.actors[self.indexInfo])
        if strLen > 17:
            begStr = self.actors[self.indexInfo][0:17]
            midStr = self.actors[self.indexInfo][17:]
            actorsL.config(text=begStr)
            #self.labelActors2.config(text=midStr)
        else:
            actorsL.config(text=self.actors[self.indexInfo])
            #self.labelActors2.config(text=' ')

        labelRate.config(text=self.rating[self.indexInfo])

        # 네이버로 열기
        self.linkL = Label(self.mainWnd, text='네이버로 열기', cursor='hand2')
        self.linkL.pack()
        self.linkL.place(x=320,y=180)
        self.linkL.bind("<Button-1>", lambda e: self.callback(self.naverlink[self.indexInfo]))

        # 관련 뉴스 - 네이버 openAPI 읽어오기
        client_id = "tvo5aUWG9rwBq1YRMqyJ"
        client_secret = "40VkT1fuAS"
        header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
        search_word = self.title[self.indexInfo] #검색어
        encode_type = 'json' #출력 방식 json 또는 xml
        max_display = 3 #출력 뉴스 수
        sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
        start = 1 # 출력 위치

        url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&sort={sort}"
        res=requests.get(url,headers=header_parms)
        datas = res.json()
        links = datas['items']
        self.link = []
        for i in links:
            self.link.append(i['link'])
        for i in range(max_display):
            string = '관련뉴스 ' + str(i+1)
            self.linkL = Label(self.mainWnd, text=string, cursor='hand2')
            self.linkL.pack()
            self.linkL.place(x=410,y=120 + i * 30)
            self.linkL.bind("<Button-1>", lambda e: self.callback(self.link[i]))


        # 영화진흥회 openAPI 읽어오기
        dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=edfd0508a0320efa8abbe1eeba097a94&movieNm="
        dayOfficeURL += self.title[self.indexInfo]
        res = requests.get(dayOfficeURL)
        text = res.text
        d = json.loads(text)
        code = []
        name = []
        genre = []
        for b in d['movieListResult']['movieList']:
            #if b['movieNm'] == self.title[self.indexInfo]:
            code.append(b['openDt'])
            name.append(b['movieNm'])
            genre.append(b['genreAlt'])
        self.labelGenre.config(text=genre)


        # 영화 이미지 띄우기
        if len(self.image) == 0:
            return

        url = self.image[self.indexInfo]
        with urllib.request.urlopen(url) as u:
            raw_data=u.read()

        im=Image.open(BytesIO(raw_data))
        global image2
        image2=ImageTk.PhotoImage(im, master=self.mainWnd)

        imgL = Label(self.mainWnd,height=100,width=100)
        imgL.pack()
        imgL.place(x=200,y=100)
        imgL.config(image=image2)

    def callback(self, url):
        webbrowser.open_new(url)
