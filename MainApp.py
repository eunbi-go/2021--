from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox
import requests
import json
from PIL import Image
from io import BytesIO
import webbrowser
import smtplib
from email.mime.text import  MIMEText
from tkinter import ttk
from bs4 import BeautifulSoup
import threading
import sys
import folium
from cefpython3 import cefpython as cef
import imp

from SearchActor import *

mainWnd = Tk()
mainWnd.geometry("900x600")
mainWnd.title("영화 정보 검색 앱")
mainWnd.configure(bg='black')




Font = font.Font(mainWnd, size=20, weight='bold', family='Consolas')

notebook = tkinter.ttk.Notebook(mainWnd, width=900,height=600)
notebook.pack()

def callback(url):
    webbrowser.open_new(url)

frameBoxOffice = Frame(mainWnd)
global photo
photo = PhotoImage(file='box.png', master=frameBoxOffice)
notebook.add(frameBoxOffice, image=photo)

frame2 = Frame(mainWnd)
global photo2
photo2 = PhotoImage(file='movie0.png', master=frameBoxOffice)
notebook.add(frame2, image=photo2)

indexInfo = 0

framePos = Frame(mainWnd)
global photo3
photo3 = PhotoImage(file='pos.png', master=framePos)
notebook.add(framePos, image=photo3)

frameMap = Frame(framePos, width=400, height=400)
frameMap.pack(side='right')



framePos.config(bg='white')

Label(framePos, text='경기도', font=("Courier",15), bg='white').place(x=10,y=10)
Label(framePos, text='군/시', font=("Courier",15), bg='white').place(x=100,y=10)

# 상영 지역
strLocation = StringVar()
combo = ttk.Combobox(framePos, textvariable=strLocation, width=10)
combo['value'] = ('가평군', '고양시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', '안양시', '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '포천시', '하남시', '화성시')
combo.current(0)
combo.pack()
combo.place(x=100,y=40)

# 영화관 리스트 박스
theaterListBox = Listbox(framePos, width=30,height=15)
theaterListBox.pack()
theaterListBox.place(x=10,y=120)

# 영화관 도로명주소
theaterL = Label(framePos, bg='white', font=('Courier', 13))
theaterL.pack()
theaterL.place(x=10,y=370)


def searchTheaters():
    strPos = strLocation.get()
    url = "https://openapi.gg.go.kr/MovieTheater?SIGUN_NM="
    url += strPos
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.find_all('row')
    global theaters
    global latitude # 위도
    global hardness # 경도
    global address
    theaters = []
    latitude = []
    hardness = []
    address = []

    cnt = 0
    theaterListBox.delete(0, END)
    for item in data:
        nm = str(item.find('bizplc_nm').string)
        lati = item.find('refine_wgs84_lat').string
        hard = item.find('refine_wgs84_logt').string
        ad = item.find('refine_roadnm_addr').string

        #theaters.append(nm)
        theaterListBox.insert(cnt, nm)
        latitude.append(lati)
        hardness.append(hard)
        address.append(ad)

        cnt += 1



def new():
    browser.Reload()
    m.save('map.html')

global ch
ch = True

def show(frame):
    global ch
    ch = False
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), [0,0,800,600])
    cef.Initialize()
    global browser
    browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
    cef.MessageLoop()



def confirmTheather():
    theatherIndex = theaterListBox.curselection()[0]
    theaterL.config(text=address[theatherIndex])
    global m
    m = folium.Map(location=[latitude[theatherIndex], hardness[theatherIndex]], zoom_start=13)
    folium.Marker([latitude[theatherIndex], hardness[theatherIndex]], popup='영화관').add_to(m)
    if ch == False:
        new()
    else:
        m.save('map.html')
        thread = threading.Thread(target=show, args=(frameMap,))
        thread.daemon = True
        thread.start()




global searchImg2
searchImg2 = PhotoImage(file='search.png')
global img
img = PhotoImage(file='conff.png')
searchBt = Button(framePos, font=('Courier',15), image=img, bg='white',
                  command=confirmTheather)
searchBt.pack()
searchBt.place(x=270,y=10)



# 영화관 찾기
global searchImg3
searchImg3 = PhotoImage(file='search.png')
searchBt = Button(framePos, font=('Courier',15), image=searchImg3, bg='white',
                  command=searchTheaters)
searchBt.pack()
searchBt.place(x=200,y=10)



# 영화 검색
frame2.config(bg='white')
movieNmEt = Entry(frame2, bd=5, bg='white')
movieNmEt.pack()
movieNmEt.place(x=15,y=40, width=100,height=40)

def search():
    strSearch = movieNmEt.get()
    movieListbox.delete(0, END)

    # 네이버 openAPI 읽어오기
    client_id = "tvo5aUWG9rwBq1YRMqyJ"
    client_secret = "40VkT1fuAS"
    header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
    url = f"https://openapi.naver.com/v1/search/movie.json?query={strSearch}"
    res=requests.get(url,headers=header_parms)

    Alldata = res.json()
    movieCnt = len(Alldata['items'])
    global title
    global naverlink
    global image
    global date
    global director
    global actors
    global rating
    title = []
    naverlink = []
    image = []
    date = []
    director = []
    actors = []
    rating = []

    for i in range(movieCnt):
        title.append(Alldata['items'][i]['title'].strip('</b>').replace('<b>','').replace('</b>',''))
        naverlink.append(Alldata['items'][i]['link'])
        image.append(Alldata['items'][i]['image'])
        date.append(Alldata['items'][i]['pubDate'])
        director.append(Alldata['items'][i]['director'].split('|')[0])
        actors.append(Alldata['items'][i]['actor'].replace('|', ', '))
        rating.append(float(Alldata['items'][i]['userRating']))

    for i in range(movieCnt):
        movieListbox.insert(i, title[i])

def showInfo():
    indexInfo = movieListbox.curselection()[0]
    labelDate.config(text=date[indexInfo])
    labelDirector.config(text=director[indexInfo])

    strActors = actors[indexInfo].split(', ')
    newStr = ''
    for i in range(len(strActors)):
        newStr += strActors[i] + '\n' + '\n'
    labelActors.config(text=newStr)
    labelRate.config(text=rating[indexInfo])

    # 네이버로 열기
    linkL = Label(frame2, text='네이버로 열기', cursor='hand2')
    linkL.pack()
    linkL.place(x=650,y=100)
    linkL.bind("<Button-1>", lambda e: callback(naverlink[indexInfo]))

    # 관련 뉴스 - 네이버 openAPI 읽어오기
    client_id = "tvo5aUWG9rwBq1YRMqyJ"
    client_secret = "40VkT1fuAS"
    header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
    search_word = title[indexInfo] #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 3 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&sort={sort}"
    res=requests.get(url,headers=header_parms)
    datas = res.json()
    links = datas['items']
    link = []
    newsTitle = []
    for i in links:
        link.append(i['link'])
        newsTitle.append(i['title'].strip('</b>').replace('<b>','').replace('</b>',''))
    for i in range(max_display):
        #string = '관련뉴스 ' + str(i+1)
        string = newsTitle[i]
        #string.strip('</b>').replace('<b>','').replace('</b>','')
        linkL = Label(frame2, text=string, cursor='hand2')
        linkL.pack()
        linkL.place(x=410,y=300 + i * 30)
        linkL.bind("<Button-1>", lambda e: callback(link[i]))


    # 영화진흥회 openAPI 읽어오기
    dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=edfd0508a0320efa8abbe1eeba097a94&movieNm="
    dayOfficeURL += title[indexInfo]
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
    labelGenre.config(text=genre)


    # 영화 이미지 띄우기
    if len(image) == 0:
        return

    url = image[indexInfo]
    with urllib.request.urlopen(url) as u:
        raw_data=u.read()

    im=Image.open(BytesIO(raw_data))
    global image2
    image2=ImageTk.PhotoImage(im, master=frame2)

    imgL = Label(frame2,height=150,width=150, bg='white')
    imgL.pack()
    imgL.place(x=550,y=100)
    imgL.config(image=image2)


def sendMail_MovieInfo():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('geunbi38@gmail.com', 'lidmnbysnqfzlfcp')
    strMain = '영화 정보 알려드립니다 - ' + str(title[indexInfo])
    strMsg = '제목 : ' + str(title[indexInfo]) + '\n' + "감독 : " + str(director[indexInfo]) + '\n' + "배우 : " + str(actors[indexInfo]) + '\n' + "평점 : " + str(rating[indexInfo])
    msg = MIMEText(strMsg)
    msg['Subject'] = strMain
    s.sendmail('nono9910@naver.com', 'geunbi38@gmail.com', msg.as_string())
    s.quit()

def sendTel_MovieInfo():
    pass

# 정보 보기 버튼
global comfirmBt
comfirmBt = PhotoImage(file='conff.png', master=frame2)
infoBt = Button(frame2, font=('Courier',15), image=comfirmBt,
                     command=showInfo, bg='white')
infoBt.place(x=270,y=30)

# 지메일 전송 버튼
global mailImg
mailImg = PhotoImage(file='mail.png', master=frame2)
mailBt = Button(frame2, font=('Courier',15), image=mailImg,
                command=sendMail_MovieInfo, bg='white')
mailBt.place(x=340,y=30)

# 영화 정보 표기
movieListbox = Listbox(frame2, width=25,height=18, relief='solid', bg='white')
movieListbox.pack()
movieListbox.place(x=10,y=90)


searchBt = Button(frame2, font=('Courier',15), image=searchImg2, bg='white',
                  command=search)
searchBt.pack()
searchBt.place(x=200,y=30)

# 개봉일
dateL = Label(frame2, text='개봉년도', font=("Courier",15), bg='white')
dateL.place(x=200,y=100)
# 평점
ratingL = Label(frame2, text='평점', font=("Courier",15), bg='white')
ratingL.place(x=200,y=130)
# 장르
genreL = Label(frame2, text='장르', font=('Courier',15), bg='white')
genreL.place(x=400,y=100)
# 감독
directorL = Label(frame2, text='감독', font=("Courier",15), bg='white')
directorL.place(x=200,y=160)
# 출연배우
actorsL = Label(frame2, text='출연배우', font=("Courier",15), bg='white')
actorsL.place(x=200,y=210)

# 개봉일
labelDate = Label(frame2, font=("Courier",15), text=' ', bg='white')
labelDate.pack()
labelDate.place(x=300,y=100)
# 평점
labelRate = Label(frame2, font=("Courier",15), text=' ', bg='white')
labelRate.pack()
labelRate.place(x=300,y=130)
# 장르
labelGenre = Label(frame2, font=('Courier',15), text=' ', bg='white')
labelGenre.pack()
labelGenre.place(x=400,y=130)
# 감독
labelDirector = Label(frame2, font=("Courier",15), text=' ', bg='white')
labelDirector.pack()
labelDirector.place(x=300,y=160)
# 출연배우
labelActors = Label(frame2, font=("Courier",15), text=' ', bg='white')
labelActors.pack()
labelActors.place(x=300,y=210)

#labelActors2 = Label(frame2, font=("Courier",10), text=' ', bg='white')
#labelActors2.pack()
#labelActors2.place(x=300,y=320)


# 배우 검색
frameActor = Frame(mainWnd)
global photoAc
photoAc = PhotoImage(file='actor.png', master=frameActor)
notebook.add(frameActor, image=photoAc)
frameActor.config(bg='white')

actorNmEt = Entry(frameActor, bd=5)
actorNmEt.pack()
actorNmEt.place(x=10,y=10, width=100,height=40)

# 영문명
Label(frameActor, text='영문명', font=("Courier",15), bg='white').place(x=20,y=100)
# 성별
Label(frameActor, text='성별', font=("Courier",15), bg='white').place(x=20,y=130)
# 영화인 분류명
Label(frameActor, text='영화인 분류', font=("Courier",15), bg='white').place(x=20,y=160)
# 필모
Label(frameActor, text='필모', font=("Courier",15), bg='white').place(x=20,y=190)

# 영문명
labelNm = Label(frameActor, font=("Courier",15), text=' ', bg='white')
labelNm.pack()
labelNm.place(x=200,y=100)
# 성별
labelSex = Label(frameActor, font=("Courier",15), text=' ', bg='white')
labelSex.pack()
labelSex.place(x=200,y=130)
# 영화인 분류
labelSort = Label(frameActor, font=("Courier",15), text=' ', bg='white')
labelSort.pack()
labelSort.place(x=200,y=160)
# 필모
actorListbox = Listbox(frameActor, width=25,height=12, relief='solid', bg='white')
actorListbox.pack()
actorListbox.place(x=0,y=220)

actorInfo = []
actorMovieNm = []
actorEgNm = []
actorSex = []
def showActorInfo():
    actorInfo = []
    actorMovieNm = []
    actorEgNm = []
    actorSex = []

    dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=edfd0508a0320efa8abbe1eeba097a94&peopleNm="
    dayOfficeURL += actorNmEt.get()
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
    for b in d['peopleInfoResult']['peopleInfo']['filmos']:
        actorMovieNm.append(b['movieNm'])

    actorInfo = d['peopleInfoResult']['peopleInfo']

    actorEgNm.append(actorInfo['sex'])
    actorSex.append(actorInfo['sex'])
    labelNm.config(text=actorInfo['peopleNmEn'])
    labelSex.config(text=actorInfo['sex'])
    labelSort.config(text=actorInfo['repRoleNm'])


    # 필모
    actorListbox.delete(0, END)
    for i in range(len(actorMovieNm)):
        actorListbox.insert(i, actorMovieNm[i])
    # self.labelFilmos.config(text=movieNm)

    # 네이버 openAPI 읽어오기
    client_id = "tvo5aUWG9rwBq1YRMqyJ"
    client_secret = "40VkT1fuAS"
    header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
    search_word = actorNmEt.get() #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 3 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&sort={sort}"
    res=requests.get(url,headers=header_parms)
    datas = res.json()
    links = datas['items']
    actorlink = []
    actorTitle = []
    for i in links:
        actorlink.append(i['link'])
        actorTitle.append(i['title'].strip('</b>').replace('<b>','').replace('</b>',''))

    string = actorTitle[0]
    actorlinkL = Label(frameActor, text=string, cursor='hand2', bg='white')
    actorlinkL.pack()
    actorlinkL.place(x=400,y=200 + 0 * 30)
    actorlinkL.bind("<Button-1>", lambda e: callback(actorlink[0]))

    string = actorTitle[1]
    actorlinkL = Label(frameActor, text=string, cursor='hand2', bg='white')
    actorlinkL.pack()
    actorlinkL.place(x=400,y=200 + 1 * 30)
    actorlinkL.bind("<Button-1>", lambda e: callback(actorlink[1]))

    string = actorTitle[2]
    actorlinkL = Label(frameActor, text=string, cursor='hand2', bg='white')
    actorlinkL.pack()
    actorlinkL.place(x=400,y=200 + 2 * 30)
    actorlinkL.bind("<Button-1>", lambda e: callback(actorlink[2]))

    # 배우 이미지
    url2 = f"https://openapi.naver.com/v1/search/image.{encode_type}?query={search_word}&display={str(int(max_display))}&sort={sort}"
    res2=requests.get(url2,headers=header_parms)
    datas2 = res2.json()
    links2 = datas2['items']
    imgLink = []
    for i in links2:
        imgLink.append(i['thumbnail'])

    imgUrl = imgLink[0]
    with urllib.request.urlopen(imgUrl) as u:
        raw_data = u.read()
    im=Image.open(BytesIO(raw_data))
    global image2
    image2=ImageTk.PhotoImage(im, master=frameActor)

    imgL = Label(frameActor,height=150,width=150, bg='white')
    imgL.pack()
    imgL.place(x=400,y=10)
    imgL.config(image=image2)

    # 배우 관련 웹문서
    url2 = f"https://openapi.naver.com/v1/search/webkr.{encode_type}?query={search_word}&display={str(int(max_display))}&sort={sort}"
    res2=requests.get(url2,headers=header_parms)
    datas2 = res2.json()
    links2 = datas2['items']
    textLink = []
    textTitle = []
    strDes = " "
    for i in links2:
        textTitle.append(i['title'].strip('</b>').replace('<b>','').replace('</b>',''))
        textLink.append(i['link'])
    textCnt = len(textLink)

    if textCnt > 0:
        string = textTitle[0]
        actorlinkL = Label(frameActor, text=string, cursor='hand2', bg='white')
        actorlinkL.pack()
        actorlinkL.place(x=600,y=50 + 0 * 30)
        strLink = textLink[0]
        actorlinkL.bind("<Button-1>", lambda e: callback(textLink[0]))
    if textCnt > 1:
        string = textTitle[1]
        actorlinkL = Label(frameActor, text=string, cursor='hand2', bg='white')
        actorlinkL.pack()
        actorlinkL.place(x=600,y=50 + 1 * 30)
        strLink = textLink[1]
        actorlinkL.bind("<Button-1>", lambda e: callback(textLink[1]))
    pass

def sendMail_ActorInfo():
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('geunbi38@gmail.com', 'lidmnbysnqfzlfcp')
    strName = actorNmEt.get()
    strMain = '배우 정보 알려드립니다 - ' + strName
    strMsg = '이름 : ' + strName + '(' + str(actorEgNm[0]) + ')' + '\n' + "성별 : " + str(actorSex[0]) + '\n'
    strMsg = strMsg + "=======참여 작품=======" + '\n'
    for i in actorMovieNm:
        strMsg += str(i) + '\n'

    msg = MIMEText(strMsg)
    msg['Subject'] = strMain
    s.sendmail('nono9910@naver.com', 'geunbi38@gmail.com', msg.as_string())
    s.quit()

# 정보 보기 버튼
infoBt = Button(frameActor, font=('Courier',15), command=showActorInfo,
                image=searchImg2, bg='white')
infoBt.place(x=130,y=10)

# 지메일 전송 버튼
actorMailBt = Button(frameActor, font=('Courier',15), image=mailImg,
                command=sendMail_ActorInfo, bg='white')
actorMailBt.place(x=200,y=10)



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

        rankingMailBt = Button(self.BoxOfficeWnd, font=('Courier',15), image=mailImg,
                             command=self.sendRankingInfo, bg='white')
        rankingMailBt.place(x=320,y=10)

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

    def sendRankingInfo(self):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('geunbi38@gmail.com', 'lidmnbysnqfzlfcp')
        strMain = '박스오피스<일간>랭킹 알려드립니다 - ' + str(self.strDate)
        strMsg = ' '
        for i in range(10):
            strMsg += str(i+1) + "위: " + str(self.movieNm[i]) + ", 개봉일: " + str(self.openingDt[i]) + '\n'
        msg = MIMEText(strMsg)
        msg['Subject'] = strMain
        s.sendmail('nono9910@naver.com', 'geunbi38@gmail.com', msg.as_string())
        s.quit()
        pass

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
        self.strDate = yearEt.get()
        if int(monthEt.get()) < 10:
            self.strDate = self.strDate + str(0) + monthEt.get()
        else:
            self.strDate += monthEt.get()
        if int(dayEt.get()) < 10:
            self.strDate = self.strDate + str(0) + dayEt.get()
        else:
            self.strDate += dayEt.get()

        dayOfficeURL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=edfd0508a0320efa8abbe1eeba097a94&targetDt="

        dayOfficeURL += self.strDate
        res = requests.get(dayOfficeURL)
        text = res.text
        d = json.loads(text)
        self.movieNm = []
        self.openingDt = []
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
            self.movieNm.append(b['movieNm'])
            self.openingDt.append(b['openDt'])
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

        # 영화 이미지 가져오기
        self.image = []
        client_id = "tvo5aUWG9rwBq1YRMqyJ"
        client_secret = "40VkT1fuAS"
        header_parms ={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
        for i in range(10):
            strSearch = self.movieNm[i]
            url = f"https://openapi.naver.com/v1/search/movie.json?query={strSearch}"
            res=requests.get(url,headers=header_parms)
            Alldata = res.json()
            movieCnt = len(Alldata['items'])

            #for j in range(movieCnt):
            self.image.append(Alldata['items'][0]['image'])


        # 순위
        with urllib.request.urlopen(self.image[self.dayRankIdx]) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        im = im.resize((80,80), Image.ANTIALIAS)
        global im1
        im1 = ImageTk.PhotoImage(im, master=self.BoxOfficeWnd)

        with urllib.request.urlopen(self.image[self.dayRankIdx+1]) as u:
            raw_data2 = u.read()
        imm = Image.open(BytesIO(raw_data2))
        imm = imm.resize((80,80), Image.ANTIALIAS)
        global im12
        im12 = ImageTk.PhotoImage(imm, master=self.BoxOfficeWnd)

        with urllib.request.urlopen(self.image[self.dayRankIdx+2]) as u:
            raw_data3 = u.read()
        immm = Image.open(BytesIO(raw_data3))
        immm = immm.resize((80,80), Image.ANTIALIAS)
        global im13
        im13 = ImageTk.PhotoImage(immm, master=self.BoxOfficeWnd)


        firstNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text='순위', bg='white')
        firstNameL.place(x=5, y=80)
        firstNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text=self.rank[self.dayRankIdx], bg='white')
        firstNameL.place(x=5, y=160)
        secondNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text=self.rank[self.dayRankIdx+1], bg='white')
        secondNameL.place(x=5, y=260)
        thirdNameL = Label(self.BoxOfficeWnd, font=("Courier",20), text=self.rank[self.dayRankIdx+2], bg='white')
        thirdNameL.place(x=5,y=360)

        # 영화 이미지
        firstNameL = Label(self.BoxOfficeWnd, image=im1)
        firstNameL.place(x=58, y=130)
        secondNameL = Label(self.BoxOfficeWnd, image=im12)
        secondNameL.place(x=58, y=230)
        thirdNameL = Label(self.BoxOfficeWnd, image=im13)
        thirdNameL.place(x=58,y=330)

        # 영화 이름
        #if len(string) > 10:
        #begStr = string[0:5]
        #midStr = string[5:]
        self.labelNm1.config(text=str(self.movieNm[self.dayRankIdx]))
        self.labelNm2.config(text=str(self.movieNm[self.dayRankIdx+1]))
        self.labelNm3.config(text=str(self.movieNm[self.dayRankIdx+2]))


        # 영화 개봉일
        firstOpenDt = Label(self.BoxOfficeWnd, text='영화 제목/개봉일', font=("Courier",17), bg='white')
        firstOpenDt.place(x=80, y=80)
        firstOpenDt = Label(self.BoxOfficeWnd, text=str(self.openingDt[self.dayRankIdx]), font=("Courier",15), bg='white')
        firstOpenDt.place(x=150, y=180)
        secondOpenDt = Label(self.BoxOfficeWnd, text=str(self.openingDt[self.dayRankIdx+1]), font=("Courier",15), bg='white')
        secondOpenDt.place(x=150, y=280)
        thirdOpenDt = Label(self.BoxOfficeWnd, text=str(self.openingDt[self.dayRankIdx+2]), font=("Courier",15), bg='white')
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

