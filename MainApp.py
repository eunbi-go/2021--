from tkinter import *
from tkinter import font
import tkinter.messagebox

mainWnd = Tk()
mainWnd.geometry("600x600")

def InitTopText():
    Font = font.Font(mainWnd, size=20, weight='bold', family='Consolas')
    mainText = Label(mainWnd, font=Font, text='영화 정보 검색 앱')
    mainText.pack()
    mainText.place(x=30)

    mainImg = tkinter.PhotoImage(file="movie0.png", master=mainWnd)
    mainImgLabel = Label(mainWnd, image=mainImg)
    mainImgLabel.pack()
    mainImgLabel.place(x=10, y=50)


InitTopText()
mainWnd.mainloop()