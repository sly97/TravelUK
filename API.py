import urllib.request
import json
from operator import itemgetter, attrgetter, methodcaller
from datetime import datetime

class API:
    __app_id = "XXX"
    __app_key = "XXX" #input app id and key from transport API
    baseURL = "http://transportapi.com/v3/"
    #api set

    def getBusStops(self, query):
        url = self.baseURL + "uk/places.json?query=" + query + "&type=bus_stop" + "&app_id=" + self.__app_id + "&app_key=" + self.__app_key #defines info needed
        result = urllib.request.urlopen(url) #creates a request object to the API
        output = result.read().decode("utf-8") #returns JSON formatted text from API
        data = json.loads(output) #converts from JSON to python array

        bus_stops = []
        for i in range(0,len(data["member"])):
            name = data["member"][i]["name"]
            lat = data["member"][i]["latitude"]
            long = data["member"][i]["longitude"]
            desc = data["member"][i]["description"]
            atco = data["member"][i]["atcocode"]
            bus_stops.append([name, lat, long, desc, atco])

            #print(bus_stops[i]) #used for testing

        return bus_stops

    def getNextBusTime(self, query):
        url = self.baseURL + "uk/bus/stop/" + query + "/live.json?app_id=" + self.__app_id + "&app_key=" + self.__app_key + "&group=route&nextbuses=yes" #defines info needed
        result = urllib.request.urlopen(url) #creates a request object to the API
        output = result.read().decode("utf-8") #returns JSON formatted text from API
        data = json.loads(output) #converts from JSON to python array

        bus_times = []
        for line in list(data["departures"]):
            for bus in data["departures"][line]:
                line = bus["line"]
                direction = bus["direction"]
                aimed_dt = bus["aimed_departure_time"]
                aimed_de = bus["best_departure_estimate"]
                bus_times.append([line, direction, aimed_dt, aimed_de])

        #for i in range(0,len(bus_times)):
            #print(bus_times[i]) #used for testing

        return bus_times

    def getTrainStations(self, query):
        url = self.baseURL + "uk/places.json?query=" + query + "&type=train_station" + "&app_id=" + self.__app_id + "&app_key=" + self.__app_key #gets info
        result = urllib.request.urlopen(url) #returns JSON formatted text from API
        output = result.read().decode("utf-8")
        data = json.loads(output)
        train_stations = []
        for i in range(0,len(data["member"])):
            name = data["member"][i]["name"]
            lat = data["member"][i]["latitude"]
            long = data["member"][i]["longitude"]
            station_code = data["member"][i]["station_code"]
            tiploc_code = data["member"][i]["tiploc_code"]
            train_stations.append([name, lat, long, station_code, tiploc_code])

            #print(train_stations[i]) #used for testing

        return train_stations

    def getNextTrainTime(self, query):
        url = self.baseURL + "uk/train/station/" + query + "/live.json?app_id=" + self.__app_id + "&app_key=" + self.__app_key + "&group=route&nextbuses=yes" #defines info needed
        result = urllib.request.urlopen(url) #creates a request object to the API
        output = result.read().decode("utf-8") #returns JSON formatted text from API
        data = json.loads(output) #converts from JSON to python array

        train_times = []
        for i in range(0,len(data["departures"]["all"])):
            operator_name = data["departures"]["all"][i]["operator"]
            arrival_time = data["departures"]["all"][i]["aimed_departure_time"]
            expected_time = data["departures"]["all"][i]["expected_departure_time"]
            origin_name = data["departures"]["all"][i]["origin_name"]
            destination_name = data["departures"]["all"][i]["destination_name"]
            train_times.append([operator_name, arrival_time, expected_time, origin_name, destination_name])

        #for i in range(0, len(train_times)):
            #print(train_times[i]) #used for testing            

        return train_times
        
    def getTubeStations(self, query):
        
        url = self.baseURL + "uk/places.json?query=" + query + "&type=tube_station" + "&app_id=" + self.__app_id + "&app_key=" + self.__app_key #gets info
        result = urllib.request.urlopen(url) #returns JSON formatted text from API
        output = result.read().decode("utf-8")
        data = json.loads(output)
        tube_stations = []
        for i in range(0,len(data["member"])):
            name = data["member"][i]["name"]
            lat = data["member"][i]["latitude"]
            long = data["member"][i]["longitude"]
            desc = data["member"][i]["description"]
            atco = data["member"][i]["atcocode"]
            tube_stations.append([name, lat, long, desc, atco])

            #print(tube_stations[i]) #used for testing

        return tube_stations

    def getJourneyInfo(self, user_from, user_to, mode):

        service = "tfl"
        route_count = 0

        while route_count == 0:
            url = self.baseURL + "uk/public/journey/from/lonlat:" + user_from + "/to/lonlat:" + user_to + ".json?app_id=" + self.__app_id + "&app_key=" + self.__app_key + "&modes=" + mode + "&service=" + service #defines info needed
            result = urllib.request.urlopen(url) #creates a request object to the API
            output = result.read().decode("utf-8") #returns JSON formatted text from API
            data = json.loads(output) #converts from JSON to python array
            routes = []
            
            if "routes" in data:
                for i in range(0, len(data["routes"])):
                    route_parts = []
                    duration = data["routes"][i]["duration"]
                    for j in range(0, len(data["routes"][i]["route_parts"])):
                        mode = data["routes"][i]["route_parts"][j]["mode"]
                        if mode == "bus":
                            from_point = data["routes"][i]["route_parts"][j]["from_point_name"]
                            to_point = data["routes"][i]["route_parts"][j]["to_point_name"]
                            dest = data["routes"][i]["route_parts"][j]["destination"]
                            duration_rp = data["routes"][i]["route_parts"][j]["duration"]
                            depart_time = data["routes"][i]["route_parts"][j]["departure_time"]
                            arrival_time = data["routes"][i]["route_parts"][j]["arrival_time"]
                            line_number = data["routes"][i]["route_parts"][j]["line_name"]
                            route_parts.append([mode, from_point, to_point, dest, depart_time, arrival_time, duration_rp,line_number])
                        elif mode != "foot":
                            from_point = data["routes"][i]["route_parts"][j]["from_point_name"]
                            to_point = data["routes"][i]["route_parts"][j]["to_point_name"]
                            dest = data["routes"][i]["route_parts"][j]["destination"]
                            duration_rp = data["routes"][i]["route_parts"][j]["duration"]
                            depart_time = data["routes"][i]["route_parts"][j]["departure_time"]
                            arrival_time = data["routes"][i]["route_parts"][j]["arrival_time"]
                            route_parts.append([mode, from_point, to_point, dest, depart_time, arrival_time, duration_rp])
                    if len(route_parts) != 0:
                        routes.append([duration, route_parts])
            
                #print(routes[i]) #used for testing

            route_count = len(routes)
            
            if route_count == 0 and service != "southeast":
                service = "southeast"
            else:
                break

        return routes

class weatherAPI:
    _key = "XXX" #input key from API
    base = "https://api.openweathermap.org/data/2.5/"
    error = ["404"]
    #api set

    def __init__(self):
        self.q = ""
        self.result = []

    def getInfo(self, q):
        self.q = q
        if self.getCurrentInfo():
            return self.error
        self.getWeekForecast()
        return self.result

    def flashReport(self):
        url = self.base + "weather?units=metric&q=London,uk&appid=" + self._key #defines info needed
        result = urllib.request.urlopen(url) #creates a request object to the API
        output = result.read().decode("utf-8") #returns JSON formatted text from API
        data = json.loads(output) #converts from JSON to python array
        return data
        
    def getCurrentInfo(self):
        try:
            url = self.base + "weather?units=metric&q=" + self.q + ",uk&appid=" + self._key #defines info needed
            result = urllib.request.urlopen(url) #creates a request object to the API
            output = result.read().decode("utf-8") #returns JSON formatted text from API
            data = json.loads(output) #converts from JSON to python array
            self.result.append(data)
        except urllib.error.HTTPError as e:
            return True

    def getWeekForecast(self):
        url = self.base + "forecast?units=metric&q=" + self.q + ",uk&appid=" + self._key #defines info needed
        result = urllib.request.urlopen(url) #creates a request object to the API
        output = result.read().decode("utf-8") #returns JSON formatted text from API
        data = json.loads(output) #converts from JSON to python array

        final = []
        for x in data["list"]:
            
            
            if "12:00:00" in x["dt_txt"]:
                stamp = x["dt"]
                dow = datetime.fromtimestamp(stamp).strftime("%A")
                forecast = {dow:[
                    x["main"]["temp"],
                    x["main"]["humidity"],
                    x["weather"][0]["description"],
                    x["wind"]["speed"]
                    ]}
                final.append(forecast)
                
        
        self.result.append(final)
