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

        # 영문명
        EngNameL = Label(self.mainWnd, text='영문명', font=("Courier",15))
        EngNameL.place(x=20,y=100)
        # 성별
        EngNameL = Label(self.mainWnd, text='성별', font=("Courier",15))
        EngNameL.place(x=20,y=130)
        # 영화인 분류명
        EngNameL = Label(self.mainWnd, text='영화인 분류', font=("Courier",15))
        EngNameL.place(x=20,y=160)
        # 관련URL
        #EngNameL = Label(self.mainWnd, text='클릭!', font=("Courier",15))
        #EngNameL.place(x=20,y=190)
        # 필모
        EngNameL = Label(self.mainWnd, text='필모', font=("Courier",15))
        EngNameL.place(x=20,y=190)

        # 영문명
        self.labelNm = Label(self.mainWnd, font=("Courier",15), text=' ')
        self.labelNm.pack()
        self.labelNm.place(x=200,y=100)
        # 성별
        self.labelSex = Label(self.mainWnd, font=("Courier",15), text=' ')
        self.labelSex.pack()
        self.labelSex.place(x=200,y=130)
        # 영화인 분류
        self.labelSort = Label(self.mainWnd, font=("Courier",15), text=' ')
        self.labelSort.pack()
        self.labelSort.place(x=200,y=160)
        # 필모
        self.labelFilmos = Label(self.mainWnd, font=("Courier",12), text=' ')
        self.labelFilmos.pack()
        self.labelFilmos.place(x=200,y=190)


    def showInfo(self):
        dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=edfd0508a0320efa8abbe1eeba097a94&peopleNm="
        dayOfficeURL += self.movieNmEt.get()
        res = requests.get(dayOfficeURL)
        text = res.text
        d = json.loads(text)
        code = ' '
        for b in d['peopleListResult']['peopleList']:
            code = b['peopleCd']

        dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?key=edfd0508a0320efa8abbe1eeba097a94&peopleCd="
        dayOfficeURL += code
        res = requests.get(dayOfficeURL)
        text = res.text
        d = json.loads(text)
        sex = []
        movieNm = []
        for b in d['peopleInfoResult']['peopleInfo']['filmos']:
            movieNm.append(b['movieNm'])
        self.info = d['peopleInfoResult']['peopleInfo']
        self.labelNm.config(text=self.info['peopleNmEn'])
        self.labelSex.config(text=self.info['sex'])
        self.labelSort.config(text=self.info['repRoleNm'])
        self.labelFilmos.config(text=movieNm)
        if self.info['homepages']:
            self.linkL = Label(self.mainWnd, text='클릭!', cursor='hand2')
            self.linkL.pack()
            self.linkL.place(x=20,y=190)
            self.linkL.bind("<Button-1>", lambda e: self.callback(self.info[self.homepages]))

        # 네이버 openAPI 읽어오기
        client_id = "tvo5aUWG9rwBq1YRMqyJ"
        client_secret = "40VkT1fuAS"
        header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
        search_word = movieNm #검색어
        encode_type = 'json' #출력 방식 json 또는 xml
        max_display = 3 #출력 뉴스 수
        sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
        start = 1 # 출력 위치

        url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&sort={sort}"
        res=requests.get(url,headers=header_parms)
        datas = res.json()
        links = datas['items']
        print(links)
        for i in links:
            print(i['link'])

    def callback(self, url):
            webbrowser.open_new(url)