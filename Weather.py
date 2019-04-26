from tkinter import *
import tkinter.messagebox as tm
import urllib.request
from tkinter import ttk
from datetime import datetime

from API import weatherAPI

class WeatherFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.check_internet()
        self.welcome_screen()

    def _homepage_btn(self):
        self.master.destroy()
        import Homepage
    #returns to the Homepage

    def cls(self):
        for x in self.winfo_children():
            x.destroy()
    #deletes screen

    def welcome_screen(self):
        self.cls()
        self.label_space0 = Label(self, text="     ", font="serif 1") #used simply to create space on screen
        self.label_status = Label(self, text="Status: " + self.internet_status, font="serif 10 bold", fg=self.fg)
        self.label_welcome = Label(self, text="Weather\nInformation", font="verdana 18 bold")
        self.label_space1 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_space2 = Label(self, text="     ", font="verdana 10") #used simply to create space on screen
        self.label_space3 = Label(self, text="                       ", font="system 10") #used simply to create space on screen
        self.label_space4 = Label(self, text=" ", font="serif 4") #used simply to create space on screen
        self.label_space9 = Label(self, text=" ", font="serif 8") #used simply to create space on screen
        #all the labels

        self.entry_place = Entry(self)
        #all the entry boxes

        self.homepage_btn = Button(self, text="<= Return to\nHomepage", font="system 10", state=self.state, command=self._homepage_btn)
        self.search_place_btn = Button(self, text="Search", font="system 9 underline", state=self.state, command=lambda:self.show_weather(self.entry_place.get()))
        self.exit_btn = Button(self, text="Exit", activebackground="cyan", activeforeground="black", font="times 12 bold", command=self._exit_btn)
        #all the buttons

        self.label_space9.grid(row=0, column=0)
        self.label_status.grid(row=1, column=1)
        self.label_welcome.grid(row=2, column=3)
        self.label_space2.grid(row=2, column=2)
        self.label_space1.grid(row=3, column=3) #used simply to create space on screen
        self.homepage_btn.grid(row=2, column=1)
        self.entry_place.grid(row=4, column=3, sticky=W)
        self.search_place_btn.grid(row=4, column=3, sticky=E)
        self.label_space3.grid(row=4, column=4) #used simply to create space on screen
        self.label_space4.grid(row=5, column=1) #used simply to create space on screen
        self.exit_btn.grid(row=6, column=3)
        #placement on the screen

        self.pack()

        self.entry_place.bind('<Return>', lambda event:self.show_weather(self.entry_place.get()))
        self.entry_place.focus()
    #first page of 'weather'
        
    def show_weather(self, q):
        if q == "":
            tm.showwarning("Warning!","Please enter a place!")
            return
        elif any(char.isdigit() for char in q):
            tm.showwarning("Warning!","Please do not enter numbers!")
            return
        elif not all(x.isalpha() or x.isspace() for x in q):
            tm.showwarning("Warning!","Please enter alphabetic characters only!")
            return

        self.App = weatherAPI()
        r = self.App.getInfo(q)
        if r[0] == "404":
            tm.showerror("Error","Sorry, no such place was found")
            return
        
        self.cls()
        self.nb = ttk.Notebook(self)

        self.homepage_btn = Button(self, text="<= Back to Search", font="system 10", state=self.state, command=self.welcome_screen)
        self.homepage_btn.grid(row=1, column=1)

        self.label_header = Label(self, text=r[0]["name"], font="verdana 14 bold underline")
        self.label_header.grid(row=1, column=2, padx=42)
        self.label_space5 = Label(self, text=" ", font="serif 10")
        self.label_space5.grid(row=2, column=1)

        self.page1 = Frame(self.nb)
        self.page2 = Frame(self.nb)
        self.page3 = Frame(self.nb)
        self.nb.add(self.page1, text="Current Weather")
        self.nb.add(self.page2, text="Weekly Forecast")
        self.nb.add(self.page3, text="Weather Map")
        self.nb.grid(row=3, column=1, rowspan=100, columnspan=100, sticky="NESW")
        #creates the 'tabs'

        #===================== C U R R E N T    W E A T H E R    B E L O W ================================

        self.label_temp = Label(self.page1, text=str(round(r[0]["main"]["temp"])) + "°", font="serif 12 bold")
        self.label_temp.grid(row=0, column=1)
        self.label_tempMin = Label(self.page1, text=str(round(r[0]["main"]["temp_min"])) + "°", font="serif 11")
        self.label_tempMin.grid(row=1, column=0)
        self.label_tempMax = Label(self.page1, text=str(round(r[0]["main"]["temp_max"])) + "°", font="serif 11")
        self.label_tempMax.grid(row=1, column=2)

        Label(self.page1, text="       ", font="serif 12").grid(row=1, column=3)
        #space between column 2 and 4

        self.label_mainDescr = Label(self.page1, text=r[0]["weather"][0]["description"], font="verdana 11")
        self.label_mainDescr.grid(row=0, column=4)
        self.label_humid = Label(self.page1, text="Humidity: " + str(round(r[0]["main"]["humidity"])) + "%", font="verdana 10")
        self.label_humid.grid(row=1, column=4)
        self.label_tempMax = Label(self.page1, text="Wind: " + str(round(r[0]["wind"]["speed"])) + " km/h", font="verdana 10")
        self.label_tempMax.grid(row=2, column=4)

        Label(self.page1, text="       ", font="serif 12").grid(row=1, column=5)
        #space between column 4 and 6

        self.label_sunrise = Label(self.page1, text="Sunrise: " + datetime.utcfromtimestamp(r[0]["sys"]["sunrise"]).strftime("%H:%M"), font="verdana 9")
        self.label_sunrise.grid(row=1, column=6)
        self.label_sunset = Label(self.page1, text="Sunset: " + datetime.utcfromtimestamp(r[0]["sys"]["sunset"]).strftime("%H:%M"), font="verdana 9")
        self.label_sunset.grid(row=2, column=6)

        #===================== W E E K L Y    F O R E C A S T    B E L O W ================================

        Label(self.page2, text="Temp", font="serif 11 bold").grid(row=1, column=0)
        Label(self.page2, text="Descr.", font="serif 11 bold").grid(row=2, column=0)
        Label(self.page2, text="Humidity", font="serif 11 bold").grid(row=3, column=0)
        Label(self.page2, text="Wind", font="serif 11 bold").grid(row=4, column=0)

        i = 1
        for x in r[1]:
            c_day = list(x.keys())[0]
            Label(self.page2, text=c_day, font="serif 12 bold underline").grid(row=0, column=i)
            Label(self.page2, text=str(round(x[c_day][0]))+"°", font="serif 10").grid(row=1, column=i)
            Label(self.page2, text=x[c_day][2], font="serif 10").grid(row=2, column=i)
            Label(self.page2, text=str(x[c_day][1])+"%", font="serif 10").grid(row=3, column=i)
            Label(self.page2, text=str(x[c_day][3])+"km/h", font="serif 10").grid(row=4, column=i)

            i = i + 1

        self.pack()
        
    def _exit_btn(self):
        self.exit_btn.flash()
        if tm.askyesno("Warning message", "Are you sure you want to exit?"):
            tm.showwarning("Exit message","You have decided to exit the program")
            self.master.destroy()
    #function of the Exit button, validates with the user first

    def check_internet(self):
        req = urllib.request.Request('http://www.google.com')
        try:
            urllib.request.urlopen(req)
            self.state = "normal"
            self.internet_status = "connected"
            self.fg = "#19EF09"
        except urllib.error.URLError as e:
            self.state = "disabled"
            self.internet_status = "not connected"
            self.fg = "red"
            self.label_statusMessage = Label(self, text="Please connect to the internet\nand restart the app", font="serif 12 bold", fg=self.fg)
            self.label_statusMessage.grid(row=1, column=2)
    #checking for internet connection
