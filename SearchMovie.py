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

        explainL = Label(self.mainWnd, text='영화 제목', font=("Courier",15))
        explainL.place(x=0,y=0)

        self.movieNmEt = Entry(self.mainWnd, bd=5)
        self.movieNmEt.pack()
        self.movieNmEt.place(x=0,y=30, width=100,height=40)

        searchBt = Button(self.mainWnd, font=('Courier',15), text='검색',
                        command=self.search)
        searchBt.pack()
        searchBt.place(x=100,y=30)

        self.mainWnd.mainloop()

    def search(self):
        self.strSearch = self.movieNmEt.get()

        client_id = "tvo5aUWG9rwBq1YRMqyJ"
        client_secret = "40VkT1fuAS"
        encText = urllib.parse.quote(self.strSearch)
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText # json 결과
        # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
