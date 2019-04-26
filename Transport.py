from tkinter import *
import tkinter.messagebox as tm
import tkinter.simpledialog as ts
import tkinter as tk
import urllib.request
from prettyprint import PrettyTable
import webbrowser

from API import API

class TransportFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.App = API()

        self.showFindBusStops = 0
        self.showFindTrainStops = 0
        self.showFindTubeStops = 0
        self.showPlanJourney = 0
        #used to trigger the 'toggle' that opens and closes pages

        self.check_internet()

        self.label_space0 = Label(self, text="     ", font="serif 1") #used simply to create space on screen
        self.label_status = Label(self, text="Status: " + self.internet_status, font="serif 10 bold", fg=self.fg)
        self.label_welcome = Label(self, text="Transport at", font="verdana 18 bold")
        self.label_welcome_at = Label(self, text="England", font="verdana 18 bold underline")
        self.label_space1 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_space2 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_space4 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_space5 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_space6 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_space7 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_space8 = Label(self, text=" ", font="serif 1") #used simply to create space on screen
        self.label_space9 = Label(self, text="     ", font="serif 1") #used simply to create space on screen
        self.label_space10 = Label(self, text="     ", font="serif 1") #used simply to create space on screen
        self.label_space11 = Label(self, text="     ", font="serif 5") #used simply to create space on screen
        #all the labels

        self.homepage_btn = Button(self, text="<= Return to Homepage", font="system 10", state=self.state, command=self._homepage_btn)
        self.busses_btn = Button(self, text="Find bus stops", font="system 10", state=self.state, fg="#009900", activebackground="#009900", activeforeground="white", command=self._FindBusStops_btn)
        self.trains_btn = Button(self, text="Find train stations", font="system 10", state=self.state, fg="#3399ff", activebackground="#3399ff", activeforeground="white", command=self._FindTrainStops_btn)
        self.tubes_btn = Button(self, text="Find tubes/undergrounds", font="system 10", state=self.state, fg="red", activebackground="red", activeforeground="white",  command=self._FindTubeStops_btn)
        self.plan_Journey_btn = Button(self, text="Plan My Journey", font="system 10", state=self.state, fg="#b33c00", activebackground="#b33c00", activeforeground="white",  command=self._PlanJourney_btn)
        self.exit_btn = Button(self, text="Exit", activebackground="cyan", activeforeground="black", font="times 12 bold", command=self._exit_btn)
        #all the buttons

        self.label_space9.grid(row=0, column=0)
        self.label_space0.grid(row=0, column=2) #used simply to create space on screen
        self.label_space10.grid(row=0, column=4) #used simply to create space on screen
        self.label_space11.grid(row=0, column=6) #used simply to create space on screen
        self.label_status.grid(row=1, column=1)
        self.label_welcome.grid(row=2, column=3)
        self.label_welcome_at.grid(row=3, column=3)
        self.label_space1.grid(row=4, column=3) #used simply to create space on screen
        self.homepage_btn.grid(row=5, column=1)
        self.label_space2.grid(row=6, column=3) #used simply to create space on screen
        self.busses_btn.grid(row=7, column=1)
        self.trains_btn.grid(row=7, column=3)
        self.tubes_btn.grid(row=7, column=5)
        self.label_space4.grid(row=8, column=5) #used simply to create space on screen
        self.label_space5.grid(row=12, column=5) #used simply to create space on screen
        self.plan_Journey_btn.grid(row=13, column=3)
        self.label_space8.grid(row=20, column=3) #used simply to create space on screen
        self.exit_btn.grid(row=29, column=3)
        #placement on the screen

        self.pack()

    def _homepage_btn(self):
        self.master.destroy()
        import Homepage
    #returns to the Homepage

    def _FindBusStops_btn(self):
        if self.showFindBusStops == 1:
            self.popUp_menu_origin_buses.destroy()
            self.label_search_By_buses.destroy()
            self.entry_query1.destroy()
            self.user_location_btn.destroy()
            self.submit_bus_stop_btn.destroy()
            self.show_map_btn.destroy()
            self.showFindBusStops = 0
        else:
            self.label_search_By_buses = Label(self, text="Search by name: ", font="serif 11 bold")
            self.label_search_By_buses.grid(row=8, column=1)
            self.entry_query1 = Entry(self)
            self.entry_query1.grid(row=9, column=1, sticky=W)
            self.user_location_btn = Button(self, text="Search", font="verdana 8 bold underline", command=self._searchBusStops)
            self.user_location_btn.grid(row=9, column=1, sticky=E)
            self.submit_bus_stop_btn = Button(self, text="Find Buses", font="serif 9 bold", command=self._FindNextBus)
            self.show_map_btn = Button(self, text="Open in Maps", font="serif 9 bold", command=lambda: self._openMapsWithCoordBus(self.select_origin_buses.get(), "Bus"))
            self.pack()
            
            self.select_origin_buses = StringVar(self.master)
            self.origin_buses_options = [""]
            self.select_origin_buses.set("Please choose a bus stop")
            self.popUp_menu_origin_buses = OptionMenu(self, self.select_origin_buses, *self.origin_buses_options)
            self.showFindBusStops = 1
    #first function to find all bus stops - asks for user's location

    def _searchBusStops(self):
        query = self.entry_query1.get()
        if query == "":
            tm.showerror("Warning","Please fill in the name of a stop")
            self.select_origin_buses.set("Please choose a bus stop")
            self.popUp_menu_origin_buses["menu"].delete(0, "end")
            return
        else:
            query = query.replace(" ", "+")
            get_info = self.App.getBusStops(query)

        self.popUp_menu_origin_buses.grid(row=10, column=1)
        self.submit_bus_stop_btn.grid(row=11, column=1, sticky=W)
        self.show_map_btn.grid(row=11, column=1, sticky=E)
        self.pack()

        self.select_origin_buses.set("Please choose a bus stop")
        self.popUp_menu_origin_buses["menu"].delete(0, "end")

        self.origin_buses_dict = {}
        for i in get_info:
            self.origin_buses_dict[i[0]] = [i[1], i[2], i[4]]
            self.popUp_menu_origin_buses["menu"].add_command(label=i[0], command=tk._setit(self.select_origin_buses,i[0]))
    #asks the user to input current/desired location, and shows all stations (bus, train or tube) withing user's input

    def _FindNextBus(self):
        query = self.select_origin_buses.get()
        if query == "Please choose a bus stop":
            tm.showinfo("Warning","Please choose a bus stop")
            return
        else:            
            requested_atco_code = self.origin_buses_dict[query][2]
            get_bus_info = self.App.getNextBusTime(requested_atco_code)
            alert = "These are the next buses for " + query + ":\n"
            table = PrettyTable()
            table.field_names = ["Bus line","Destination","Expected","Actual"]
            for i in range(0, len(get_bus_info)):
                line = get_bus_info[i][0]
                dest = get_bus_info[i][1]
                if len(dest) > 15:
                    dest = dest[0:15] + ".."
                exp = get_bus_info[i][2]
                act = get_bus_info[i][3]
                #alert = alert + str(get_bus_info[i]) + "\n"
                table.add_row([line, dest, exp, act])
            tm.showinfo("Buses Times for: " + query ,table)
            #print(table) #used for testing
    #finds next times for the specified bus
            
    def _openMapsWithCoordBus(self, key, service):
        if key == "Please choose a bus stop" or key == "Please choose a train station" or key == "Please choose a tube station":
            return
        if service == "Bus":
            dictionary = self.origin_buses_dict[key]
        elif service == "Train":
            dictionary = self.origin_trains_dict[key]
        elif service == "Tube":
            dictionary = self.origin_tubes_dict[key]

        lat = dictionary[0]
        long = dictionary[1]
        url = "https://www.google.co.uk/maps/@" + str(lat) + "," + str(long) + ",18z"
        path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
        webbrowser.get(path).open(url)
    #opens in Google Maps the location of the requested station/stop
        
    def _FindTrainStops_btn(self):
        if self.showFindTrainStops == 1:
            self.popUp_menu_origin_trains.destroy()
            self.label_search_By.destroy()
            self.entry_query2.destroy()
            self.search_train_btn.destroy()
            self.submit_train_station_btn.destroy()
            self.show_train_map_btn.destroy()
            self.showFindTrainStops = 0
        else:
            self.label_search_By = Label(self, text="Search by name: ", font="serif 11 bold")
            self.label_search_By.grid(row=8, column=3)
            self.entry_query2 = Entry(self)
            self.entry_query2.grid(row=9, column=3, sticky=W)
            self.search_train_btn = Button(self, text="Search", font="verdana 8 bold underline", command=self._searchTrainStops_btn)
            self.search_train_btn.grid(row=9, column=3, sticky=E)
            self.submit_train_station_btn = Button(self, text="Find Trains", font="serif 9 bold", command=self._FindNextTrain)
            self.show_train_map_btn = Button(self, text="Open in Maps", font="serif 9 bold", command=lambda: self._openMapsWithCoordBus(self.select_origin_trains.get(), "Train"))
            self.pack()

            self.select_origin_trains = StringVar(self.master)
            self.origin_trains_options = [""]
            self.select_origin_trains.set("Please choose a train station")
            self.popUp_menu_origin_trains = OptionMenu(self, self.select_origin_trains, *self.origin_trains_options)
            self.showFindTrainStops = 1
    #first function to find train stations - asks for user's location

    def _searchTrainStops_btn(self):
        query = self.entry_query2.get()
        if query == "":
            tm.showerror("Warning","Please fill in the name of a stop")
            self.select_origin_trains.set("Please choose a train station")
            self.popUp_menu_origin_trains["menu"].delete(0, "end")
            return
        else:
            query = query.replace(" ", "+")
            get_info = self.App.getTrainStations(query)

        self.popUp_menu_origin_trains.grid(row=10, column=3)
        self.submit_train_station_btn.grid(row=11, column=3, sticky=W)
        self.show_train_map_btn.grid(row=11, column=3, sticky=E)
        self.pack()

        self.select_origin_trains.set("Please choose a train station")
        self.popUp_menu_origin_trains["menu"].delete(0, "end")

        self.origin_trains_dict = {}
        for i in get_info:
            self.origin_trains_dict[i[0]] = [i[1], i[2], i[3]]
            self.popUp_menu_origin_trains["menu"].add_command(label=i[0], command=tk._setit(self.select_origin_trains,i[0]))
    #second function to find all train stations - within user's input

    def _FindNextTrain(self):
        query = self.select_origin_trains.get()
        if query == "Please choose a train station":
            tm.showinfo("Warning","Please choose a train station")
            return
        else:            
            requested_trainATCO_code = self.origin_trains_dict[query][2]
            get_train_info = self.App.getNextTrainTime(requested_trainATCO_code)
            alert = "These are the trains at " + query + ":\n"
            table = PrettyTable()
            table.field_names = ["Operator","Arrival","Expected","Origin","Dest."]
            for i in range(0, len(get_train_info)):
                oper_name = get_train_info[i][0]
                arr_time = get_train_info[i][1]
                expect_time = get_train_info[i][2]
                origin = get_train_info[i][3]
                if len(origin) > 12:
                    origin = origin[0:12] + ".."
                dest = get_train_info[i][4]
                if len(dest) > 12:
                    dest = dest[0:12] + ".."
                table.add_row([oper_name, arr_time, expect_time, origin, dest])
            tm.showinfo("Train Times for: " + query ,table)
            #print(table) #used for testing
    #finds next times for the specified bus

    def _FindTubeStops_btn(self):
        if self.showFindTubeStops == 1:
            self.popUp_menu_origin_tubes.destroy()
            self.label_searchBy_tube.destroy()
            self.entry_query3.destroy()
            self.search_btn.destroy()
            self.submit_tube_station_btn.destroy()
            self.show_tube_map_btn.destroy()
            self.showFindTubeStops = 0
        else:
            self.label_searchBy_tube = Label(self, text="Search by name: ", font="serif 11 bold")
            self.label_searchBy_tube.grid(row=8, column=5)
            self.entry_query3 = Entry(self)
            self.entry_query3.grid(row=9, column=5, sticky=W)
            self.search_btn = Button(self, text="Search", font="verdana 8 bold underline", command=self._searchTubeStops_btn)
            self.search_btn.grid(row=9, column=5, sticky=E)
            self.submit_tube_station_btn = Button(self, text="Find Next Tube", font="serif 9 bold", state="disabled", cursor="X_cursor")
            self.show_tube_map_btn = Button(self, text="Open in Maps", font="serif 9 bold", command=lambda: self._openMapsWithCoordBus(self.select_origin_tubes.get(), "Tube"))
            self.pack()

            self.select_origin_tubes = StringVar(self.master)
            self.origin_tubes_options = [""]
            self.select_origin_tubes.set("Please choose a tube station")
            self.popUp_menu_origin_tubes = OptionMenu(self, self.select_origin_tubes, *self.origin_tubes_options)
            self.showFindTubeStops = 1
    #first function to find tube stations - ask for user's input

    def _searchTubeStops_btn(self):
        query = self.entry_query3.get()
        if query == "":
            tm.showerror("Warning","Please fill in the name of a stop")
            self.select_origin_tubes.set("Please choose a tube station")
            self.popUp_menu_origin_tubes["menu"].delete(0, "end")
            return
        else:
            query = query.replace(" ", "+")
            get_info = self.App.getTubeStations(query)

        self.popUp_menu_origin_tubes.grid(row=10, column=5)
        self.submit_tube_station_btn.grid(row=11, column=5, sticky=W)
        self.show_tube_map_btn.grid(row=11, column=5, sticky=E)
        self.pack()

        self.select_origin_tubes.set("Please choose a tube station")
        self.popUp_menu_origin_tubes["menu"].delete(0, "end")

        self.origin_tubes_dict = {}
        for i in get_info:
            self.origin_tubes_dict[i[0]] = [i[1], i[2]]
            self.popUp_menu_origin_tubes["menu"].add_command(label=i[0], command=tk._setit(self.select_origin_tubes,i[0]))
    #second function to find all tube stations within user's input

    def _PlanJourney_btn(self):
        if self.showPlanJourney == 1:
            self.label_from.destroy()
            self.chooseOrigin_btn.destroy()
            self.label_to.destroy()
            self.chooseDestination_btn.destroy()
            self.label_type.destroy()
            self.searchRoute_btn.destroy()
            self.popUp_menu.destroy()
            self.popUp_menu_origin.destroy()
            self.popUp_menu_dest.destroy()
            self.showPlanJourney = 0
        else:
            self.label_space6.grid(row=14, column=2) #used simply to create space on screen
            self.label_from = Label(self, text="From:", font="serif 10 bold underline")
            self.label_from.grid(row=15, column=3)
            self.chooseOrigin_btn = Button(self, text="Enter Place\nof Origin", font="times 11 bold", command=self._askOrigin)
            self.chooseOrigin_btn.grid(row=16, column=3)
            self.label_to = Label(self, text="To:", font="serif 10 bold underline")
            self.label_to.grid(row=15, column=5)
            self.chooseDestination_btn = Button(self, text="Enter Place\nof Destination", font="times 11 bold", command=self._askDestination)
            self.chooseDestination_btn.grid(row=16, column=5)
            self.label_type = Label(self, text="Transport Type:", font="serif 10 bold underline")
            self.label_type.grid(row=15, column=1)
            
            self.select = StringVar(self.master)
            options = ["Bus", "Train", "Tube/Underground"]
            self.select.set("Bus")
            self.popUp_menu = OptionMenu(self, self.select, *options, command=self._chnageJourneyType)
            self.popUp_menu.grid(row=16, column=1)

            self.selectOrigin = StringVar(self.master)
            origin_options = [""]
            self.selectOrigin.set("Please choose a\nplace of origin")
            self.popUp_menu_origin = OptionMenu(self, self.selectOrigin, *origin_options)
            self.popUp_menu_origin.grid(row=17, column=3)

            self.selectDestination = StringVar(self.master)
            dest_options = [""]
            self.selectDestination.set("Please choose your\ndestination")
            self.popUp_menu_dest = OptionMenu(self, self.selectDestination, *dest_options)
            self.popUp_menu_dest.grid(row=17, column=5)

            self.label_space7.grid(row=18, column=2) #used simply to create space on screen
            
            self.searchRoute_btn = Button(self, text="Search Route", font="times 11 bold", fg="#ff9900", activebackground="#ff9900", activeforeground="white", command=self._searchRoute_btn)
            self.searchRoute_btn.grid(row=19, column=5)
            self.pack()
            self.showPlanJourney = 1
    #function showing the details and inputs needed for the user to plan a journey

    def _chnageJourneyType(self, value):
        self.selectOrigin.set("Please choose a\nplace of origin")
        self.selectDestination.set("Please choose your\ndestination")
        self.popUp_menu_origin["menu"].delete(0, "end")
        self.popUp_menu_dest["menu"].delete(0, "end")
    #resets all inputs (with the 'Plan a Journey' page) if user changes type of transport

    def _askOrigin(self):
        route_type = self.select.get()
        answer = ""
        while answer == "":
            answer = ts.askstring("Place of Origin","Please write your port/place of origin:")
            if answer is None:
                return
            elif answer == "":
                tm.showinfo("Error","Please write your place of origin")
            else:
                answer = answer.replace(" ", "+")
                if route_type == "Bus":
                    self.origin_places = self.App.getBusStops(answer)
                elif route_type == "Train":
                    self.origin_places = self.App.getTrainStations(answer)
                elif route_type == "Tube/Underground":
                    self.origin_places = self.App.getTubeStations(answer)

        self.selectOrigin.set("Please choose a\nplace of origin")
        self.popUp_menu_origin["menu"].delete(0, "end")

        self.origin_dict = {}
        for i in self.origin_places:
            self.origin_dict[i[0]] = [i[1], i[2]]
            self.popUp_menu_origin["menu"].add_command(label=i[0], command=tk._setit(self.selectOrigin,i[0]))
    #asks the user to input current/desired location, and shows all stations (bus, train or tube) withing user's input
        
    def _askDestination(self):
        route_type = self.select.get()
        answer = ""
        while answer == "":
            answer = ts.askstring("Place of Destination","Please write your destination place:")
            if answer is None:
                return
            elif answer == "":
                tm.showinfo("Error","Please write your destination place")
            else:
                answer = answer.replace(" ", "+")
                if route_type == "Bus":
                    self.dest_places = self.App.getBusStops(answer)
                elif route_type == "Train":
                    self.dest_places = self.App.getTrainStations(answer)
                elif route_type == "Tube/Underground":
                    self.dest_places = self.App.getTubeStations(answer)

        self.selectDestination.set("Please choose your\ndestination")
        self.popUp_menu_dest["menu"].delete(0, "end")

        self.destination_dict = {}
        for i in self.dest_places:
            self.destination_dict[i[0]] = [i[1], i[2]]
            self.popUp_menu_dest["menu"].add_command(label=i[0], command=tk._setit(self.selectDestination,i[0]))
    #asks the user to input their destination location, and shows all stations (bus, train or tube) withing user's input

    def _searchRoute_btn(self):
        origin_chosen = self.selectOrigin.get()
        destination_chosen = self.selectDestination.get()
        transport_type = self.select.get().lower()

        if origin_chosen == "Please choose a\nplace of origin" or destination_chosen == "Please choose your\ndestination":
            tm.showinfo("Warning","Please choose both origin and destination stops")
            return
        elif origin_chosen == destination_chosen:
            tm.showinfo("Warning","Origin and destination must be different")
            return
        else:
            tm.showinfo("Info","Your chosen route:\n" + "From: " + origin_chosen + "\nTo:      " + destination_chosen + "\nBy:      " + transport_type)

            origin_coord_lat = self.origin_dict[origin_chosen][0]
            origin_coord_long = self.origin_dict[origin_chosen][1]
            final_origin_coord = str(origin_coord_long) + "," + str(origin_coord_lat) ##

            dest_coord_lat = self.destination_dict[destination_chosen][0]
            dest_coord_long = self.destination_dict[destination_chosen][1]
            final_dest_coord = str(dest_coord_long) + "," + str(dest_coord_lat) ##

            #print(final_origin_coord)
            #print(final_dest_coord)

            get_route_info = self.App.getJourneyInfo(final_origin_coord, final_dest_coord, transport_type)
            if len(get_route_info) == 0:
                tm.showinfo("Warning","Sorry, no routes were found")
            else:
                showframe = Tk()
                showframe.title("Route Information")
                showframe.resizable(False, False)
                bf = showResults(showframe,get_route_info)
                showframe.mainloop()
    #function for calculating and displaying the route for selected criterias
        
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

class showResults(Frame):
    def __init__(self, master, results):
        super().__init__(master)

        self.label_from = Label(self, text="From:", font="verdana 12 bold underline")
        self.label_to = Label(self, text="To:", font="verdana 12 bold underline")
        self.label_dest = Label(self, text="Destination:", font="verdana 12 bold underline")
        self.label_depart = Label(self, text="Departure:", font="verdana 12 bold underline")
        self.label_arrive = Label(self, text="Arrival:", font="verdana 12 bold underline")
        self.label_dur = Label(self, text="Duration:", font="verdana 12 bold underline")
        self.exit_btn1 = Button(self, text="Exit", activebackground="cyan", activeforeground="black", font="times 12 bold", command=master.destroy)

        self.label_from.grid(row=1, column=1)
        self.label_to.grid(row=1, column=2)
        self.label_dest.grid(row=1, column=3)
        self.label_depart.grid(row=1, column=4)
        self.label_arrive.grid(row=1, column=5)
        self.label_dur.grid(row=1, column=6)
        self.exit_btn1.grid(row=100, column=3, sticky=E)

        grow = 2

        for i in range(0, len(results)):
            for j in range(0, len(results[i][1])):
                grow = grow+2
                extra = ""
                
                if j == len(results[i][1]):
                    extra = " underline"
                if results[i][1][j][0] == "bus":
                    self.label_from = Label(self, text="Line:", font="verdana 12 bold underline")
                    self.label_from.grid(row=1, column=0)
                    rp_line = Label(self, text=results[i][1][j][7], font="verdana 10")
                    rp_line.grid(row=grow, column=0)
                
                rp_from = Label(self, text=results[i][1][j][1], font=str("verdana 10"+extra))
                rp_to = Label(self, text=results[i][1][j][2], font="verdana 10")
                rp_dest = Label(self, text=results[i][1][j][3], font="verdana 10")
                rp_depart = Label(self, text=results[i][1][j][4], font="verdana 10")
                rp_arrive = Label(self, text=results[i][1][j][5], font="verdana 10")
                rp_dur = Label(self, text=results[i][1][j][6], font="verdana 10")
                
                rp_from.grid(row=grow, column=1)
                rp_to.grid(row=grow, column=2)
                rp_dest.grid(row=grow, column=3)
                rp_depart.grid(row=grow, column=4)
                rp_arrive.grid(row=grow, column=5)
                rp_dur.grid(row=grow, column=6)

            space = Label(self, text=" ")
            space.grid(row=grow+1, column=1)

        self.pack()
