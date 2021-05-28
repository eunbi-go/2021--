from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox
import requests
import json
from PIL import Image
from io import BytesIO
import webbrowser
from SearchMovie import *
from SearchActor import *

mainWnd = Tk()
mainWnd.geometry("900x600")
mainWnd.title("영화 정보 검색 앱")
mainWnd.configure(bg='black')

Font = font.Font(mainWnd, size=20, weight='bold', family='Consolas')

notebook = tkinter.ttk.Notebook(mainWnd, width=900,height=600)
notebook.pack()

frameBoxOffice = Frame(mainWnd)
global photo
photo = PhotoImage(file='box.png', master=frameBoxOffice)
notebook.add(frameBoxOffice, image=photo)


frame2 = Frame(mainWnd)
global photo2
photo2 = PhotoImage(file='movie0.png', master=frameBoxOffice)
notebook.add(frame2, image=photo2)

# 영화 검색
movieNmEt = Entry(frame2, bd=5)
movieNmEt.pack()
movieNmEt.place(x=100,y=100, width=100,height=40)

searchBt = Button(frame2, font=('Courier',15), text='검색',
                  command=SearchMovie.search)
searchBt.pack()
searchBt.place(x=220,y=30)

# 정보 보기 버튼
infoBt = Button(frame2, font=('Courier',15), text='정보보기',
                     command=SearchMovie.showInfo)
infoBt.place(x=290,y=30)

# 영화 정보 표기
movieListbox = Listbox(frame2, width=25,height=18, relief='solid')
movieListbox.pack()
movieListbox.place(x=0,y=90)

# 개봉일
dateL = Label(frame2, text='개봉년도', font=("Courier",15))
dateL.place(x=200,y=200)
# 평점
ratingL = Label(frame2, text='평점', font=("Courier",15))
ratingL.place(x=200,y=230)
# 장르
genreL = Label(frame2, text='장르', font=('Courier',15))
genreL.place(x=400,y=230)
# 감독
directorL = Label(frame2, text='감독', font=("Courier",15))
directorL.place(x=200,y=260)
# 출연배우
actorsL = Label(frame2, text='출연배우', font=("Courier",15))
actorsL.place(x=200,y=290)

# 개봉일
labelDate = Label(frame2, font=("Courier",15), text=' ')
labelDate.pack()
labelDate.place(x=300,y=200)
# 평점
labelRate = Label(frame2, font=("Courier",15), text=' ')
labelRate.pack()
labelRate.place(x=300,y=230)
# 장르
labelGenre = Label(frame2, font=('Courier',10), text=' ')
labelGenre.pack()
labelGenre.place(x=450,y=230)
# 감독
labelDirector = Label(frame2, font=("Courier",15), text=' ')
labelDirector.pack()
labelDirector.place(x=300,y=260)
# 출연배우
labelActors = Label(frame2, font=("Courier",10), text=' ')
labelActors.pack()
labelActors.place(x=300,y=290)

labelActors2 = Label(frame2, font=("Courier",10), text=' ')
labelActors2.pack()
labelActors2.place(x=300,y=320)

class BoxOfficeRank:
    def __init__(self, frame):
        self.dayRankIdx = 0
        # 막대 그래프
        self.graphW = 800
        self.graphH = 600
        self.graphBar = (self.graphW-10)/10
        self.graphStart = False

        self.BoxOfficeWnd = frame
        self.BoxOfficeWnd.config(bg='white')
        tmpFont = font.Font(self.BoxOfficeWnd, size=20, weight='bold', family='Consolas')

        global yearEt, monthEt, dayEt
        yearEt = Entry(self.BoxOfficeWnd, bd=5, selectborderwidth=1)
        monthEt = Entry(self.BoxOfficeWnd, bd=5)
        dayEt = Entry(self.BoxOfficeWnd, bd=5)

        yearEt.pack()
        yearEt.place(x=15, y=25, width=50, height=40)
        monthEt.pack()
        monthEt.place(x=65, y=25, width=50, height=40)
        dayEt.pack()
        dayEt.place(x=115, y=25, width=50, height=40)

        global searchImg
        searchImg = PhotoImage(file='search.png')
        searchBt = Button(self.BoxOfficeWnd, font=tmpFont,
                          image=searchImg, command=self.ShowRank)
        searchBt.pack()
        searchBt.place(x=180, y=10)

        global nextImg
        nextImg = PhotoImage(file='next.png', master=self.BoxOfficeWnd)
        nextBt = Button(self.BoxOfficeWnd, font=tmpFont, text='다음', command=self.NextPage, image=nextImg)
        nextBt.pack()
        nextBt.place(x=840,y=200)

        global preImg
        preImg = PhotoImage(file='pre.png', master=self.BoxOfficeWnd)
        preBt = Button(self.BoxOfficeWnd, font=tmpFont, text='이전', command=self.PrePage, image=preImg)
        preBt.pack()
        preBt.place(x=10,y=200)

        global graphImg
        graphImg = PhotoImage(file='graph.png', master=self.BoxOfficeWnd)
        graphBt = Button(self.BoxOfficeWnd, font=tmpFont, text='그래프', command=self.BoxOfficeGraph, image=graphImg)
        graphBt.pack()
        graphBt.place(x=250,y=10)

        # 영화 제목
        self.labelNm1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelNm1.pack()
        self.labelNm1.place(x=150,y=150)
        self.labelNm2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelNm2.pack()
        self.labelNm2.place(x=150,y=250)
        self.labelNm3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelNm3.pack()
        self.labelNm3.place(x=150,y=350)

        self.labelAcc1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelAcc1.pack()
        self.labelAcc1.place(x=380,y=150)
        self.labelAcc2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelAcc2.pack()
        self.labelAcc2.place(x=380,y=250)
        self.labelAcc3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelAcc3.pack()
        self.labelAcc3.place(x=380,y=350)

        self.labelAud1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelAud1.pack()
        self.labelAud1.place(x=540,y=150)
        self.labelAud2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelAud2.pack()
        self.labelAud2.place(x=540,y=250)
        self.labelAud3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelAud3.pack()
        self.labelAud3.place(x=540,y=350)

        self.labelDayScn1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelDayScn1.pack()
        self.labelDayScn1.place(x=670,y=150)
        self.labelDayScn2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelDayScn2.pack()
        self.labelDayScn2.place(x=670,y=250)
        self.labelDayScn3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelDayScn3.pack()
        self.labelDayScn3.place(x=670,y=350)

        self.labelDayCnt1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelDayCnt1.pack()
        self.labelDayCnt1.place(x=770,y=150)
        self.labelDayCnt2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelDayCnt2.pack()
        self.labelDayCnt2.place(x=770,y=250)
        self.labelDayCnt3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ', bg='white')
        self.labelDayCnt3.pack()
        self.labelDayCnt3.place(x=770,y=350)

        self.BoxOfficeWnd.mainloop()

    def BoxOfficeGraph(self):
        self.Graph = Tk()
        self.currGrp = 0

        self.canvas = Canvas(self.Graph, width=self.graphW, height=self.graphH, bg='white')
        self.canvas.pack()

        self.chkVar = IntVar()
        self.chkBox = Radiobutton(self.Graph, text='상영횟수/스크린수', variable=self.chkVar,
                                  value=1, command=self.DrawGraph)
        self.chkBox.pack(anchor=W)
        self.chkBox2 = Radiobutton(self.Graph, text='누적관객수/누적매출액', variable=self.chkVar,
                                   value=2, command=self.DrawGraph2)
        self.chkBox2.pack(anchor=W)

    def DrawGraph(self):
        self.canvas.delete('scrnCnt2')
        for i in range(10):
            self.canvas.create_text(30+i*self.graphBar, 595, text=str(i+1), font=('Courier',18), tags='scrnCnt')
            # 해당 일자 상영된 횟수
            self.canvas.create_rectangle(10+i*self.graphBar, self.graphH-(self.graphH-20)*(self.iShowCnt[i])/(max(self.iShowCnt)),
                                         10+(i+1)*self.graphBar-50, self.graphH-20, fill='red', tags='scrnCnt')
            # 해당 일자 상영한 스크린 수
            self.canvas.create_rectangle(10+i*self.graphBar+50, self.graphH-(self.graphH-20)*(self.iScrnCnt[i])/(max(self.iScrnCnt)),
                                         10+(i+1)*self.graphBar-50, self.graphH-20, fill='blue', tags='scrnCnt')
        # 설명
        self.canvas.create_text(600,50,text='상영횟수',font=('Courier',15),fill='blue',tags='scrnCnt')
        self.canvas.create_text(700,50,text='스크린수',font=('Courier',15),fill='red',tags='scrnCnt')


    def DrawGraph2(self):
        self.canvas.delete('scrnCnt')
        for i in range(10):
            self.canvas.create_text(30+i*self.graphBar, 595, text=str(i+1), font=('Courier',18), tags='scrnCnt2')
            # 해당 일자 상영된 횟수
            self.canvas.create_rectangle(10+i*self.graphBar, self.graphH-(self.graphH-20)*(self.iAudiAc[i])/(max(self.iAudiAc)),
                                         10+(i+1)*self.graphBar-50, self.graphH-20, fill='red', tags='scrnCnt2')
            # 해당 일자 상영한 스크린 수
            self.canvas.create_rectangle(10+i*self.graphBar+50, self.graphH-(self.graphH-20)*(self.iSalesAcc[i])/(max(self.iSalesAcc)),
                                         10+(i+1)*self.graphBar-50, self.graphH-20, fill='blue', tags='scrnCnt2')
        self.canvas.create_text(600,50,text='누적매출액',font=('Courier',15),fill='blue',tags='scrnCnt2')
        self.canvas.create_text(730,50,text='누적관객수',font=('Courier',15),fill='red',tags='scrnCnt2')

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
        self.rank = []
        self.iRank = []
        self.salesAcc = []
        self.iSalesAcc = []
        self.audiAcc = []
        self.iAudiAc = []
        self.scrnCnt = []
        self.iScrnCnt = []
        self.showCnt = []
        self.iShowCnt = []
        for b in d['boxOfficeResult']['dailyBoxOfficeList']:
            movieNm.append(b['movieNm'])
            openingDt.append(b['openDt'])
            self.rank.append(b['rank'])
            self.iRank.append(int(b['rank']))
            self.salesAcc.append(b['salesAcc'])
            self.iSalesAcc.append(int(b['salesAcc']))
            self.audiAcc.append(b['audiAcc'])
            self.iAudiAc.append(int(b['audiAcc']))
            self.scrnCnt.append(b['scrnCnt'])
            self.iScrnCnt.append(int(b['scrnCnt']))
            self.showCnt.append(b['showCnt'])
            self.iShowCnt.append((int)(b['showCnt']))
        NmFont = font.Font(mainWnd, size=30, weight='bold', family='Consolas')

        # 순위
        firstNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text='순위', bg='white')
        firstNameL.place(x=50, y=80)
        firstNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text=self.rank[self.dayRankIdx], bg='white')
        firstNameL.place(x=60, y=160)
        secondNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text=self.rank[self.dayRankIdx+1], bg='white')
        secondNameL.place(x=60, y=260)
        thirdNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text=self.rank[self.dayRankIdx+2], bg='white')
        thirdNameL.place(x=60,y=360)

        # 영화 이름
        #if len(string) > 10:
        #begStr = string[0:5]
        #midStr = string[5:]
        self.labelNm1.config(text=movieNm[self.dayRankIdx])
        self.labelNm2.config(text=movieNm[self.dayRankIdx+1])
        self.labelNm3.config(text=movieNm[self.dayRankIdx+2])


        # 영화 개봉일
        firstOpenDt = Label(self.BoxOfficeWnd, text='영화 제목/개봉일', font=("Courier",17), bg='white')
        firstOpenDt.place(x=135, y=80)
        firstOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx], font=("Courier",15), bg='white')
        firstOpenDt.place(x=150, y=180)
        secondOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx+1], font=("Courier",15), bg='white')
        secondOpenDt.place(x=150, y=280)
        thirdOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx+2], font=("Courier",15), bg='white')
        thirdOpenDt.place(x=150, y=380)

        # 누적 매출액
        firstOpenDt = Label(self.BoxOfficeWnd, text='누적 매출액', font=("Courier",12), bg='white')
        firstOpenDt.place(x=380, y=80)
        self.labelAcc1.config(text=self.salesAcc[self.dayRankIdx])
        self.labelAcc2.config(text=self.salesAcc[self.dayRankIdx+1])
        self.labelAcc3.config(text=self.salesAcc[self.dayRankIdx+2])

        # 누적 관객수
        firstOpenDt = Label(self.BoxOfficeWnd, text='누적 관객수', font=("Courier",12), bg='white')
        firstOpenDt.place(x=540, y=80)
        self.labelAud1.config(text=self.audiAcc[self.dayRankIdx])
        self.labelAud2.config(text=self.audiAcc[self.dayRankIdx+1])
        self.labelAud3.config(text=self.audiAcc[self.dayRankIdx+2])

        # 해당 일자 상영한 스크린 수
        firstOpenDt = Label(self.BoxOfficeWnd, text='당일 스크린', font=("Courier",12), bg='white')
        firstOpenDt.place(x=655, y=60)
        firstOpenDt = Label(self.BoxOfficeWnd, text='상영 수', font=("Courier",12), bg='white')
        firstOpenDt.place(x=675, y=80)
        self.labelDayScn1.config(text=self.scrnCnt[self.dayRankIdx])
        self.labelDayScn2.config(text=self.scrnCnt[self.dayRankIdx+1])
        self.labelDayScn3.config(text=self.scrnCnt[self.dayRankIdx+2])

        # 해당 일자 상영된 횟수
        firstOpenDt = Label(self.BoxOfficeWnd, text='당일 상영', font=("Courier",12), bg='white')
        firstOpenDt.place(x=760, y=60)
        firstOpenDt = Label(self.BoxOfficeWnd, text='횟수', font=("Courier",12), bg='white')
        firstOpenDt.place(x=780, y=80)
        self.labelDayCnt1.config(text=self.showCnt[self.dayRankIdx])
        self.labelDayCnt2.config(text=self.showCnt[self.dayRankIdx+1])
        self.labelDayCnt3.config(text=self.showCnt[self.dayRankIdx+2])


BoxOfficeRank(frameBoxOffice)



mainWnd.mainloop()

