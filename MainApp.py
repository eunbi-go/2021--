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
        self.dayRankIdx = 0


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

        nextBt = Button(self.BoxOfficeWnd, font=tmpFont, text='다음', command=self.NextPage)
        nextBt.pack()
        nextBt.place(x=300,y=10)

        preBt = Button(self.BoxOfficeWnd, font=tmpFont, text='이전', command=self.PrePage)
        preBt.pack()
        preBt.place(x=350,y=10)

        self.BoxOfficeWnd.mainloop()

    def NextPage(self):
        self.dayRankIdx += 1
        self.ShowRank()

    def PrePage(self):
        self.dayRankIdx -= 1
        self.ShowRank()

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
        openingDt = []
        salesAcc = []
        audiAcc = []
        scrnCnt = []
        showCnt = []
        for b in d['boxOfficeResult']['dailyBoxOfficeList']:
            movieNm.append(b['movieNm'])
            openingDt.append(b['openDt'])
            salesAcc.append(b['salesAcc'])
            audiAcc.append(b['audiAcc'])
            scrnCnt.append(b['scrnCnt'])
            showCnt.append(b['showCnt'])

        NmFont = font.Font(mainWnd, size=30, weight='bold', family='Consolas')

        # 영화 이름
        firstNameL = Label(self.BoxOfficeWnd, text=movieNm[self.dayRankIdx], font=NmFont)
        firstNameL.place(x=150, y=100)
        secondNameL = Label(self.BoxOfficeWnd, text=movieNm[self.dayRankIdx+1], font=NmFont)
        secondNameL.place(x=150, y=200)
        thirdNameL = Label(self.BoxOfficeWnd, text=movieNm[self.dayRankIdx+2], font=NmFont)
        thirdNameL.place(x=150,y=300)

        # 영화 개봉일
        firstOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx], font=NmFont)
        firstOpenDt.place(x=150, y=150)
        secondOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx+1], font=NmFont)
        secondOpenDt.place(x=150, y=250)
        thirdOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx+2], font=NmFont)
        thirdOpenDt.place(x=150, y=350)

        # 누적 매출액
        firstSales = Label(self.BoxOfficeWnd, text=salesAcc[self.dayRankIdx], font=NmFont)
        firstSales.place(x=380, y=100)
        secondSales = Label(self.BoxOfficeWnd, text=salesAcc[self.dayRankIdx+1], font=NmFont)
        secondSales.place(x=380, y=200)
        thirdSales = Label(self.BoxOfficeWnd, text=salesAcc[self.dayRankIdx+2], font=NmFont)
        thirdSales.place(x=380, y=300)

        # 누적 관객수
        firstSales = Label(self.BoxOfficeWnd, text=audiAcc[self.dayRankIdx], font=NmFont)
        firstSales.place(x=500, y=100)
        secondSales = Label(self.BoxOfficeWnd, text=audiAcc[self.dayRankIdx+1], font=NmFont)
        secondSales.place(x=500, y=200)
        thirdSales = Label(self.BoxOfficeWnd, text=audiAcc[self.dayRankIdx+2], font=NmFont)
        thirdSales.place(x=500, y=300)

        # 해당 일자 상영한 스크린 수
        firstSales = Label(self.BoxOfficeWnd, text=scrnCnt[self.dayRankIdx], font=NmFont)
        firstSales.place(x=600, y=100)
        secondSales = Label(self.BoxOfficeWnd, text=scrnCnt[self.dayRankIdx+1], font=NmFont)
        secondSales.place(x=600, y=200)
        thirdSales = Label(self.BoxOfficeWnd, text=scrnCnt[self.dayRankIdx+2], font=NmFont)
        thirdSales.place(x=600, y=300)

        # 해당 일자 상영된 횟수
        firstSales = Label(self.BoxOfficeWnd, text=showCnt[self.dayRankIdx], font=NmFont)
        firstSales.place(x=700, y=100)
        secondSales = Label(self.BoxOfficeWnd, text=showCnt[self.dayRankIdx+1], font=NmFont)
        secondSales.place(x=700, y=200)
        thirdSales = Label(self.BoxOfficeWnd, text=showCnt[self.dayRankIdx+2], font=NmFont)
        thirdSales.place(x=700, y=300)

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