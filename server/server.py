from os import truncate
import socket
import json
from threading import Thread
from datetime import date
import random

# helper functions
def checkExistUsername(username):
    for user in userData:
        if userData[user]["username"] == username:
            return True
    return False

def createNewUser(username, password):
    global userData
    newUser = {len(userData): {"username": username,"password": password}}
    with open("user.json", "r+") as file:
        fileData = json.load(file)
        fileData.update(newUser)
        file.seek(0)
        json.dump(fileData, file, indent = 4)
        userData = fileData

def checkLogIn(username, password):
    for user in userData.values():
        if user["username"] == username and user["password"] == password:
            try:
                user['isAdmin']
                return "isAdmin"
            except: return "isUser"
    return False

def checkExistsCity(cityName):
    for city in cityData.values():
        if city["cityName"] == cityName:
            return True
    return False

def getWeatherByCity(city, numDay):
    res = "\n"
    day_loop = DAY
    month_loop = MONTH
    year_loop = YEAR

    if (int(DAY) - numDay - 1 < 0):
        index = MONTHS.index(MONTH)
        PrevMonth = MONTHS[index-1]
        keys = list(weatherData[YEAR][PrevMonth])
        lastDayofPrevMonth = keys[-1]

    for i in range(numDay):
        try:
            date_data = weatherData[year_loop][month_loop][day_loop]
            if (date_data[city]):
                weather = date_data[city]
        except:
            weather = "null"

        res += "%-5s %s, %s: %s\n" % (month_loop,day_loop.zfill(2), year_loop,weather)
        day_loop = str(int(day_loop) - 1)
        if (int(day_loop) <= 0):
            day_loop = lastDayofPrevMonth
            month_loop = PrevMonth
    return res

def getWeatherByCityJson(city, numDay):
    res = '{"%s": {' % (city)
    day_loop = DAY
    month_loop = MONTH
    year_loop = YEAR

    if (int(DAY) - numDay - 1 < 0):
        index = MONTHS.index(MONTH)
        PrevMonth = MONTHS[index-1]
        keys = list(weatherData[YEAR][PrevMonth])
        lastDayofPrevMonth = keys[-1]

    for i in range(numDay):
        try:
            date_data = weatherData[year_loop][month_loop][day_loop]
            city = city.replace(" ", "")
            if (date_data[city]):
                weather = date_data[city]
        except:
            weather = "null"

        res += '"%s %s %s": "%s",' % (month_loop,day_loop.zfill(2), year_loop,weather)
        day_loop = str(int(day_loop) - 1)
        if (int(day_loop) <= 0):
            day_loop = lastDayofPrevMonth
            month_loop = PrevMonth

    res = res[:-1]
    res += "}}"
    return res

def getWeatherByDate(day, month, year):
    allCity = list(cityData)
    try:
        date_data = weatherData[year][month][day]
    except:
        return "No data available"
    res = "\n"
    for city in allCity:
        try:
            status = date_data[city]
        except:
            status = "null"
        res += "%s: %s\n" % (cityData[city]['cityName'], status)
    return res

def commandManager(commandArr):
    print(commandArr)
    data_transfer = "Error"
    if commandArr[0] == "/help":
        data_transfer= "\n/city [city_name]\n[city_name]: TPHCM, HaNoi, DaNang, Hue"
    if (commandArr[0] == "/list"):
        data_transfer = getWeatherByDate(commandArr[1], commandArr[2], commandArr[3])
    if (commandArr[0] == "/city"):
        data_transfer = getWeatherByCity(commandArr[1],7)
    if (commandArr[0] == "/getCity"):
        data_transfer = getAllCity()


    return data_transfer

def getAllCity():
    temp = list(cityData)
    res = ""
    for city in temp:
        res += cityData[city]['cityName'] + "\n"
    print(res)
    res = res[:-1]
    return res

def createNewCity(cityName):
    global cityData
    keyCity = cityName.replace(" ", "")
    newCity= {keyCity: {"cityName": cityName}}
    with open("city.json", "r+") as file:
        fileData = json.load(file)
        fileData.update(newCity)
        file.seek(0)
        json.dump(fileData, file, indent = 4)
        cityData = fileData

def checkExistsDate(day, month, year):
    try:
        weatherData[year][month][day]
        return True
    except:
        return False

def getWeather(day, month, year, cityName):
    cityName = cityName.replace(" ", "")
    if checkExistsDate(day, month ,year):
        try:
            weather = weatherData[year][month][day][cityName]
            return weather
        except:
            return False
    else: return False

def getAllCities(day, month, year):
    res = '{"%s %s %s": {' % (month, day, year)
    for city in cityData.values():
        weather = getWeather(day, month, year, city["cityName"])
        if weather == False: weather = "null"
        res += '"%s": "%s",' % (city["cityName"], weather)
    res = res[:-1]
    res += '}}'
    return res

def updateWeatherByDate(newData):
    try:
        data = json.loads(newData)
        print(data)
        dataDate = list(data.keys())
        dataDate = dataDate[0]
        dataDate = dataDate.split()
        dataCity = list(data.values())
        dataCity = dataCity[0]

        cityList = {}
        for city in dataCity:
            if(dataCity[city] != "null"):
                cityKey = city.replace(" ", "")
                cityList[cityKey] = dataCity[city]

        year = dataDate[2]
        month = dataDate[0]
        day = dataDate[1]

        try: weatherData[year]
        except: weatherData[year] = {}
        try: weatherData[year][month]
        except: weatherData[year][month] = {}

        weatherData[year][month][day] = cityList
        weatherJson = open("weather.json", "w")
        json.dump(weatherData, weatherJson)

        return True
    except:
        print("Error updating to json file")
        return False

def updateWeatherByCity(newData):
    data = json.loads(newData)
    print(data)

    city = list(data.keys())
    city = city[0].replace(" ", "")
    weatherList = list(data.values())
    weatherList = weatherList[0]

    try:
        for weather in weatherList:
            date = weather.split()
            year = date[2]
            month = date[0]
            day = date[1]
            weatherData[year][month][day][city] = weatherList[weather]

        weatherJson = open("weather.json", "w")
        json.dump(weatherData, weatherJson)
        return True

    except:
        print("Error updating to json file")
        return False

def getCityList():
    res = '{'
    for city in cityData.keys():
        res += '"%s": "%s",' % (city, cityData[city]["cityName"])
    res = res[:-1]
    res += '}'
    return res

# server functions
def acceptClientConnections():
    while True:
        client, clientAddr = server.accept()
        print(clientAddr, "has connected")
        clientAddrs[client] = clientAddr
        Thread(target=processClientReq, args=(client, clientAddr,)).start()

def receiveUserReq(client, clientAddr):
    try:
        clientReq = client.recv(1024)
        strclientReq = clientReq.decode("utf8")
        data = strclientReq.split()
        return data
    except:
        disconnectClient(client, clientAddr)
        return False

def receiveAdminReq(client, clientAddr):
    try:
        clientReq = client.recv(1024)
        strclientReq = clientReq.decode("utf8")
        data = strclientReq.split("\n")
        return data
    except:
        disconnectClient(client, clientAddr)
        return False

def disconnectClient(client, clientAddr):
    print(clientAddr, "has disconnected")
    client.close()
    del clientAddrs[client]

def processClientReq(client, clientAddr):
    clientType = logInSection(client, clientAddr)
    if clientType == "user":
        userSection(client, clientAddr)
    elif clientType == "admin":
        adminSection(client, clientAddr)

# section functions
def logInSection(client, clientAddr):
    while True:
        data = receiveUserReq(client, clientAddr)
        if data:
            reqType = data[0]
            if reqType == "signin":
                print(clientAddr ,"SIGN IN")
                if len(data) == 3:
                    username = data[1]
                    password = data[2]
                    userType = checkLogIn(username, password)
                    if userType != False:
                        client.sendall(bytes("success", "utf8"))
                        print(clientAddr, "SIGN IN: success")
                        return "user"
                    else:
                        client.sendall(bytes("fail", "utf8"))
                        print(clientAddr, "SIGN IN: info incorrect")
                else:
                    client.sendall(bytes("syntax", "utf8"))
                    print(clientAddr, "SIGN IN: syntax error")

            elif reqType == "signup":
                print(clientAddr, "SIGN UP")
                if len(data) == 3:
                    username = data[1]
                    password = data[2]
                    if checkExistUsername(username) == False:
                        createNewUser(username, password)
                        client.sendall(bytes("success", "utf8"))
                        print(clientAddr, "SIGN UP: success")
                        return "user"
                    else:
                        client.sendall(bytes("fail", "utf8"))
                        print(clientAddr, "SIGN UP: username already existed")
                else:
                    client.sendall(bytes("syntax", "utf8"))
                    print(clientAddr, "SIGN UP: syntax error")

            elif reqType == "signinadmin":
                print(clientAddr, "SIGN IN ADMIN")
                if len(data) == 3:
                    username = data[1]
                    password = data[2]
                    userType = checkLogIn(username, password)
                    if userType == "isAdmin":
                        client.sendall(bytes("success", "utf8"))
                        print(clientAddr, "SIGN IN ADMIN: success")
                        return "admin"
                    else:
                        client.sendall(bytes("info incorrect", "utf8"))
                        print(clientAddr, "SIGN IN ADMIN: info incorrect")
                else:
                    client.sendall(bytes("syntax error", "utf8"))
                    print(clientAddr, "SIGN IN ADMIN: syntax error")

            elif reqType == "exit":
                disconnectClient(client, clientAddr)
                return False

            else:
                client.sendall(bytes("unknown command", "utf8"))
                print(clientAddr, "unknown command")
        else: return False

def userSection(client, clientAddr):
    while True:
        data = receiveUserReq(client, clientAddr)
        if data:
            reqType = data[0]
            if reqType == "exit":
                disconnectClient(client, clientAddr)
                return

            response = commandManager(data)
            client.sendall(bytes(response, "utf8"))
            print(clientAddr, response)

        else: return

def adminSection(client, clientAddr):
    while True:
        data = receiveAdminReq(client, clientAddr)
        if data:
            reqType = data[0]
            if reqType == "addcity":
                print(clientAddr, "ADMIN ADD CITY")
                if len(data) == 2:
                    newCityName = data[1]
                    if checkExistsCity(newCityName) == False:
                        createNewCity(newCityName)
                        client.sendall(bytes("success", "utf8"))
                        print(clientAddr, "ADMIN ADD CITY: success")

                    else:
                        client.sendall(bytes("city already existed", "utf8"))
                        print(clientAddr, "ADMIN ADD CITY: city already existed")

                else:
                    client.sendall(bytes("syntax error", "utf8"))
                    print(clientAddr, "ADMIN ADD CITY: syntax error")

            elif reqType == "choosedate":
                print(clientAddr, "ADMIN CHOOSE DATE: ", data)
                res = getAllCities(data[1], data[2], data[3])
                print(res)
                client.sendall(bytes(res, "utf8"))
                print("ADMIN CHOOSE DATE: city list sent successfully")

            elif reqType == "updateddate":
                print(clientAddr, "ADMIN UPDATE BY DATE")
                if updateWeatherByDate(data[1]):
                    client.sendall(bytes("success", "utf8"))
                    print("ADMIN UPDATE BY DATE: updated successfully")
                else:
                    client.sendall(bytes("error", "utf8"))
                    print("ADMIN UPDATE BY DATE: error")

            elif reqType == "getcitylist":
                print(clientAddr, "ADMIN GET CITY LIST")
                res = getCityList()
                client.sendall(bytes(res, "utf8"))

            elif reqType == "choosecity":
                print(clientAddr, "ADMIN CHOOSE CITY: ", data[1])
                res = getWeatherByCityJson(data[1], 7)
                print(res)
                client.sendall(bytes(res, "utf8"))
                print("success")

            elif reqType == "updatedcity":
                print(clientAddr, "ADMIN UPDATE BY CITY")
                if updateWeatherByCity(data[1]):
                    client.sendall(bytes("success", "utf8"))
                    print("ADMIN UPDATE BY CITY: updated successfully")
                else:
                    client.sendall(bytes("error", "utf8"))
                    print("ADMIN UPDATE BY CITY: error")

            elif reqType == "exit":
                disconnectClient(client, clientAddr)
                return

            else:
                client.sendall(bytes("Unknown command", "utf8"))
                print(clientAddr, "Unknown command")

        else: return False

def generateRandomWeather():
    weatherType = ['Rainy', 'Sunny', 'Cloudy', 'Windy', 'Snowy']
    for year in weatherData:
        for month in weatherData[year]:
            for day in  weatherData[year][month]:
                for city in cityData:
                    weatherIndex = random.randint(0, len(weatherType)-1)
                    weatherData[year][month][day][city] = weatherType[weatherIndex]
    with open("weather.json", "w") as outfile:
        json.dump(weatherData, outfile)

# main function
if __name__ == "__main__":
    today = date.today()
    DAY = today.strftime("%d")
    MONTH = today.strftime("%B")
    YEAR = today.strftime("%Y")
    MONTHS = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "Setemper", "October", "November", "December"]

    clientAddrs = {}

    userJson = open("user.json")
    weatherJson = open("weather.json")
    cityJson = open("city.json")

    userData = json.load(userJson)
    weatherData = json.load(weatherJson)
    cityData = json.load(cityJson)

    #generateRandomWeather()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = socket.gethostname()
    if (hostname == "MACs-MacBook-Pro.local"):
        hostname = "localhost"
    HOST = socket.gethostbyname(hostname)
    PORT = 65432

    print("Server IP: ", HOST)
    server.bind((HOST, PORT))

    server.listen(5)
    print("Server 1 is online, wating for connections...")

    acceptClientConnections()
    server.close()
