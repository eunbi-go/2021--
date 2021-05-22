from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox

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
        self.BoxOfficeWnd.mainloop()
        pass

MainGUI()