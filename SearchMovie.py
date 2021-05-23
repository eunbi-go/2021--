from tkinter import *
from tkinter import font
import tkinter.ttk
import tkinter.messagebox
import requests
import json

class SearchMovie:
    def __init__(self):
        self.mainWnd = Tk()
        self.mainWnd.geometry("600x400")
        self.mainWnd.title("영화 검색")
        self.mainWnd.mainloop()