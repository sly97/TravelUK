from tkinter import *
import tkinter.messagebox as tm
import urllib.request
from API import weatherAPI

class HomepageFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.wApp = weatherAPI()

        self.master = master
        self.check_internet()

        self.label_space0 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_status = Label(self, text="Status: " + self.internet_status, font="serif 10 bold", fg=self.fg)
        self.label_welcome = Label(self, text="Welcome to Travel At", font="verdana 18 bold")
        self.label_welcomeAt = Label(self, text="England", font="verdana 18 bold underline")
        self.label_space1 = Label(self, text=" ", font="serif 8") #used simply to create space on screen
        self.label_menu = Label(self, text="| Menu: |", font="serif 16 bold underline")
        self.label_LocalNews = Label(self, text="| Local News: |", font="serif 16 bold underline")
        self.label_weather = Label(self, text="| Weather: |", font="serif 16 bold underline")
        self.label_space2 = Label(self, text=" ", font="serif 8") #used simply to create space on screen
        #all the labels

        self.transport_btn = Button(self, text="Transport", fg='green', activebackground="green", activeforeground="white", font="system 10", state=self.state, command=self._transport_btn)
        self.parking_btn = Button(self, text="Parking", fg='blue', activebackground="blue", activeforeground="white", font="system 10", state=self.state, command=self._parking_btn)
        self.LocalNews_btn = Button(self, text="Local News", fg='red', activebackground="red", activeforeground="white", font="system 10", state="disabled", cursor="X_cursor", command=self._LocalNews_btn)
        self.weather_btn = Button(self, text="Weather", fg='#FF8000', activebackground="#FF8000", activeforeground="white", font="system 10", state=self.state, command=self._weather_btn)
        self.moreNews_btn = Button(self, text="More local news", fg='red', activebackground="red", activeforeground="white", font="system 11", state="disabled", cursor="X_cursor", command=self._LocalNews_btn)
        self.moreWeather_btn = Button(self, text="More Weather info", fg='#FF8000', activebackground="#FF8000", activeforeground="white", font="system 11", state=self.state, command=self._weather_btn)
        self.exit_btn = Button(self, text="Exit", activebackground="cyan", activeforeground="black", font="times 12 bold", command=self._exit_btn)
        #all the buttons

        current_Lon_Temp = str(round(self.wApp.flashReport()["main"]["temp"]))
        Label(self, text=current_Lon_Temp+"°\nLondon", font="serif 11 bold").grid(row=6, column=3)

        self.label_space0.grid(row=0, column=2) #used simply to create space on screen
        self.label_status.grid(row=1, column=1)
        self.label_welcome.grid(row=2, column=2)
        self.label_welcomeAt.grid(row=3, column=2)
        self.label_space1.grid(row=4, column=2) #used simply to create space on screen
        self.label_menu.grid(row=5, column=1)
        self.transport_btn.grid(row=6, column=1)
        self.parking_btn.grid(row=7, column=1)
        self.LocalNews_btn.grid(row=8, column=1)
        self.weather_btn.grid(row=9, column=1)
        self.label_LocalNews.grid(row=5, column=2)
        self.moreNews_btn.grid(row=7, column=2)
        self.label_weather.grid(row=5, column=3)
        self.moreWeather_btn.grid(row=7, column=3)
        self.exit_btn.grid(row=19, column=2)
        self.label_space2.grid(row=20, column=2) #used simply to create space on screen
        #placement on the screen

        self.pack()

    def _transport_btn(self):
        self.master.destroy()
        from Transport import TransportFrame
        trans = Tk()
        trans.title("Transport")
        #trans.state('zoomed') #fit monitor's size
        lf = TransportFrame(trans)
        trans.mainloop()
    #function for the Transprt page, open it in a new window (continuously)
        
    def _parking_btn(self):
        root.destroy()
        import Parking
    #function for the Parking page, open it in a new window (continuously)

    def _LocalNews_btn(self):
        root.destroy()
        import LocalNews
    #function for the Local News page, open it in a new window (continuously)

    def _weather_btn(self):
        self.master.destroy()
        from Weather import WeatherFrame
        weath = Tk()
        weath.title("Weather")
        #trans.state('zoomed') #fit monitor's size
        lf = WeatherFrame(weath)
        weath.mainloop()
    #function for the Weather page, open it in a new window (continuously)

    def _exit_btn(self):
        self.exit_btn.flash()
        if tm.askyesno("Warning message", "Are you sure you want to exit?"):
            tm.showwarning("Exit message","You have decided to exit the program")
            root.destroy()
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
           
root = Tk()
root.title("Homepage")
lf = HomepageFrame(root)
root.mainloop()
