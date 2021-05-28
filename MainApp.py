from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox
import requests
import json
from PIL import Image
from SearchMovie import *
from SearchActor import *

mainWnd = Tk()
mainWnd.geometry("800x600")
mainWnd.title("영화 정보 검색 앱")
#mainWnd.configure(bg='black')


Font = font.Font(mainWnd, size=20, weight='bold', family='Consolas')
mainText = Label(mainWnd, font=Font, text='영화 정보 검색 앱')
mainText.pack()
mainText.place(x=30)

notebook = tkinter.ttk.Notebook(mainWnd, width=800,height=600)
notebook.pack()

frameBoxOffice = Frame(mainWnd)
notebook.add(frameBoxOffice, text='박스오피스')

class BoxOfficeRank:
    def __init__(self):
        self.dayRankIdx = 0
        # 막대 그래프
        self.graphW = 800
        self.graphH = 600
        self.graphBar = (self.graphW-10)/10
        self.graphStart = False

        self.BoxOfficeWnd = frameBoxOffice
        #self.BoxOfficeWnd.geometry("1000x500")
        #self.BoxOfficeWnd.title("박스 오피스 순위")
        tmpFont = font.Font(self.BoxOfficeWnd, size=20, weight='bold', family='Consolas')

        frame = Frame(self.BoxOfficeWnd)
        frame.pack()
        global yearEt, monthEt, dayEt
        yearEt = Entry(self.BoxOfficeWnd, bd=5, selectborderwidth=1)
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

        graphBt = Button(self.BoxOfficeWnd, font=tmpFont, text='그래프', command=self.BoxOfficeGraph)
        graphBt.pack()
        graphBt.place(x=400,y=10)

        # 영화 제목
        self.labelNm1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelNm1.pack()
        self.labelNm1.place(x=150,y=100)
        self.labelNm2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelNm2.pack()
        self.labelNm2.place(x=150,y=200)
        self.labelNm3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelNm3.pack()
        self.labelNm3.place(x=150,y=300)

        self.labelAcc1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelAcc1.pack()
        self.labelAcc1.place(x=380,y=100)
        self.labelAcc2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelAcc2.pack()
        self.labelAcc2.place(x=380,y=200)
        self.labelAcc3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelAcc3.pack()
        self.labelAcc3.place(x=380,y=300)

        self.labelAud1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelAud1.pack()
        self.labelAud1.place(x=540,y=100)
        self.labelAud2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelAud2.pack()
        self.labelAud2.place(x=540,y=200)
        self.labelAud3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelAud3.pack()
        self.labelAud3.place(x=540,y=300)

        self.labelDayScn1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelDayScn1.pack()
        self.labelDayScn1.place(x=670,y=100)
        self.labelDayScn2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelDayScn2.pack()
        self.labelDayScn2.place(x=670,y=200)
        self.labelDayScn3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelDayScn3.pack()
        self.labelDayScn3.place(x=670,y=300)

        self.labelDayCnt1 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelDayCnt1.pack()
        self.labelDayCnt1.place(x=770,y=100)
        self.labelDayCnt2 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelDayCnt2.pack()
        self.labelDayCnt2.place(x=770,y=200)
        self.labelDayCnt3 = Label(self.BoxOfficeWnd, font=("Courier",15), text=' ')
        self.labelDayCnt3.pack()
        self.labelDayCnt3.place(x=770,y=300)

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
        firstNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text='순위')
        firstNameL.place(x=25, y=60)
        rankFont = font.Font(family="Courier", size=16, weight="bold", slant="italic")
        firstNameL = Label(self.BoxOfficeWnd, font=("Courier",40), text=self.rank[self.dayRankIdx])
        firstNameL.place(x=30, y=100)
        secondNameL = Label(self.BoxOfficeWnd, font=("Courier",40), text=self.rank[self.dayRankIdx+1])
        secondNameL.place(x=30, y=200)
        thirdNameL = Label(self.BoxOfficeWnd, font=("Courier",40), text=self.rank[self.dayRankIdx+2])
        thirdNameL.place(x=30,y=300)

        # 영화 이름
        #if len(string) > 10:
        #begStr = string[0:5]
        #midStr = string[5:]
        self.labelNm1.config(text=movieNm[self.dayRankIdx])
        self.labelNm2.config(text=movieNm[self.dayRankIdx+1])
        self.labelNm3.config(text=movieNm[self.dayRankIdx+2])


        # 영화 개봉일
        firstOpenDt = Label(self.BoxOfficeWnd, text='영화 제목 / 개봉일', font=("Courier",15))
        firstOpenDt.place(x=140, y=60)
        firstOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx], font=NmFont)
        firstOpenDt.place(x=150, y=130)
        secondOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx+1], font=NmFont)
        secondOpenDt.place(x=150, y=230)
        thirdOpenDt = Label(self.BoxOfficeWnd, text=openingDt[self.dayRankIdx+2], font=NmFont)
        thirdOpenDt.place(x=150, y=330)

        # 누적 매출액
        firstOpenDt = Label(self.BoxOfficeWnd, text='누적 매출액', font=("Courier",12))
        firstOpenDt.place(x=380, y=60)
        self.labelAcc1.config(text=self.salesAcc[self.dayRankIdx])
        self.labelAcc2.config(text=self.salesAcc[self.dayRankIdx+1])
        self.labelAcc3.config(text=self.salesAcc[self.dayRankIdx+2])

        # 누적 관객수
        firstOpenDt = Label(self.BoxOfficeWnd, text='누적 관객수', font=("Courier",12))
        firstOpenDt.place(x=540, y=60)
        self.labelAud1.config(text=self.audiAcc[self.dayRankIdx])
        self.labelAud2.config(text=self.audiAcc[self.dayRankIdx+1])
        self.labelAud3.config(text=self.audiAcc[self.dayRankIdx+2])

        # 해당 일자 상영한 스크린 수
        firstOpenDt = Label(self.BoxOfficeWnd, text='당일 스크린', font=("Courier",12))
        firstOpenDt.place(x=655, y=40)
        firstOpenDt = Label(self.BoxOfficeWnd, text='상영 수', font=("Courier",12))
        firstOpenDt.place(x=675, y=60)
        self.labelDayScn1.config(text=self.scrnCnt[self.dayRankIdx])
        self.labelDayScn2.config(text=self.scrnCnt[self.dayRankIdx+1])
        self.labelDayScn3.config(text=self.scrnCnt[self.dayRankIdx+2])

        # 해당 일자 상영된 횟수
        firstOpenDt = Label(self.BoxOfficeWnd, text='당일 상영', font=("Courier",12))
        firstOpenDt.place(x=760, y=40)
        firstOpenDt = Label(self.BoxOfficeWnd, text='횟수', font=("Courier",12))
        firstOpenDt.place(x=780, y=60)
        self.labelDayCnt1.config(text=self.showCnt[self.dayRankIdx])
        self.labelDayCnt2.config(text=self.showCnt[self.dayRankIdx+1])
        self.labelDayCnt3.config(text=self.showCnt[self.dayRankIdx+2])






label1 = Button(frameBoxOffice, text='박스오피스', command=BoxOfficeRank)
label1.pack()




frame2 = Frame(mainWnd)
notebook.add(frame2, text='영화검색')

label2 = Label(frame2, text='영화')
label2.pack()

        # 이미지
        #global photo
        #photo = PhotoImage(file='movie0.png', master=mainWnd)
        #photoL = Label(mainWnd, image=photo)
        #photoL.pack()
        #photoL.place(x=0,y=0)

mainWnd.mainloop()

