from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox
import requests
import json

mainWnd = Tk()
mainWnd.geometry("600x600")
mainWnd.title("영화 정보 검색 앱")



class MainGUI:
    def __init__(self):
        Font = font.Font(mainWnd, size=20, weight='bold', family='Consolas')
        mainText = Label(mainWnd, font=Font, text='영화 정보 검색 앱')
        mainText.pack()
        mainText.place(x=30)

        self.SetButton()
        mainWnd.mainloop()

    def SetButton(self):
        tmpFont = font.Font(mainWnd, size=15, weight='bold', family='Consolas')
        self.boxOffice = Button(mainWnd, text='박스 오피스 순위', font=tmpFont, command=self.BoxOffice, width=15, height=5)
        self.boxOffice.place(x=0, y=40)

    def BoxOffice(self):
        self.BoxOfficeWnd = Tk()
        self.BoxOfficeWnd.geometry("1000x500")
        self.BoxOfficeWnd.title("박스 오피스 순위")
        tmpFont = font.Font(mainWnd, size=20, weight='bold', family='Consolas')

        frame = Frame(self.BoxOfficeWnd)
        frame.pack()
        global yearEt, monthEt, dayEt
        yearEt = Entry(self.BoxOfficeWnd, bd=5)
        monthEt = Entry(self.BoxOfficeWnd, bd=5)
        dayEt = Entry(self.BoxOfficeWnd, bd=5)

        yearEt.pack()
        yearEt.place(x=10, y=10, width=50, height=40)
        monthEt.pack()
        monthEt.place(x=60, y=10, width=50, height=40)
        dayEt.pack()
        dayEt.place(x=110, y=10, width=50, height=40)

        searchBt = Button(self.BoxOfficeWnd, font=tmpFont, text='검색', command=self.ShowRank)
        searchBt.pack()
        searchBt.place(x=180, y=10)

        self.BoxOfficeWnd.mainloop()

    def ShowRank(self):
        strDate = yearEt.get()
        if int(monthEt.get()) < 10:
            strDate = strDate + str(0) + monthEt.get()
        else:
            strDate += monthEt.get()
        if int(dayEt.get()) < 10:
            strDate = strDate + str(0) + dayEt.get()
        else:
            strDate += dayEt.get()

        dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=edfd0508a0320efa8abbe1eeba097a94&targetDt="

        dayOfficeURL += strDate
        res = requests.get(dayOfficeURL)
        text = res.text
        d = json.loads(text)
        movieNm = []
        for b in d['boxOfficeResult']['dailyBoxOfficeList']:
            movieNm.append(b['movieNm'])
        self.dayRankIdx = 0
        firstNameL = Label(self.BoxOfficeWnd, text = movieNm[self.dayRankIdx])
        firstNameL.place(x=150, y=100)
        secondNameL = Label(self.BoxOfficeWnd, text=movieNm[self.dayRankIdx+1])
        secondNameL.place(x=150, y=200)
        thirdNameL = Label(self.BoxOfficeWnd, text=movieNm[self.dayRankIdx+2])
        thirdNameL.place(x=150,y=300)

        self.rankImg = []
        self.rankImg.append(PhotoImage(file='first.GIF', master=self.BoxOfficeWnd))
        self.rankImg.append(PhotoImage(file='second.GIF', master=self.BoxOfficeWnd))
        self.rankImg.append(PhotoImage(file='third.GIF', master=self.BoxOfficeWnd))

        self.imgLable = []
        for i in range(3):
            self.imgLable.append(Label(self.BoxOfficeWnd, image=self.rankImg[i]))
            self.imgLable[i].pack()
            self.imgLable[i].place(x=10, y=50+i*160)




MainGUI()