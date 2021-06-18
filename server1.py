#import libraries
from os import truncate
import socket
import json
from threading import Thread
from datetime import date

# functions
def checkExistUsername(username):
    for user in userData["users"]:
        if userData["users"][user]["username"] == username:
            return True
    return False

def createNewUser(username, password):
    userJson = open("user.json")
    userData = json.load(userJson)
    newUser = {len(userData["users"]): {"username": username,"password": password}}
    with open("user.json", "r+") as file:
        fileData = json.load(file)
        fileData["users"].update(newUser)
        file.seek(0)
        json.dump(fileData, file, indent = 4)

def checkLogIn(username, password):
    userJson = open("user.json")
    userData = json.load(userJson)
    for user in userData["users"].values():
        if user["username"] == username and user["password"] == password:
            try:
                user['isAdmin']
                return "isAdmin"
            except: return "isUser"
    return False

def checkExistsCity(cityName):
    cityJson = open("city.json")
    cityData = json.load(cityJson)
    for city in cityData["cities"].values():
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
            weather = "NaN"

        res += "%-5s %s, %s: %s\n" % (month_loop,day_loop.zfill(2), year_loop,weather)
        day_loop = str(int(day_loop) - 1)
        if (int(day_loop) <= 0):
            day_loop = lastDayofPrevMonth
            month_loop = PrevMonth
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
            status = "NaN"
        res += "%s: %s\n" % (city, status)
    return res

def commandManager(commandArr):
    print(commandArr)
    if commandArr[0] == "/help":
        return "\n/city [city_name]\n[city_name]: TPHCM, HaNoi, DaNang, Hue"
    if (commandArr[0] == "/list"):
        data_transfer = getWeatherByDate(commandArr[1], commandArr[2], commandArr[3])
        return data_transfer
    if (commandArr[0] == "/city"):
        data_transfer = getWeatherByCity(commandArr[1],7)
        return data_transfer
    else:
        return "unknown command"
def createNewCity(cityName):
    cityJson = open("city.json")
    cityData = json.load(cityJson)
    newCity= {len(cityData["cities"]): {"cityName": cityName}}
    with open("city.json", "r+") as file:
        fileData = json.load(file)
        fileData["cities"].update(newCity)
        file.seek(0)
        json.dump(fileData, file, indent = 4)

def checkExistsDate(day, month ,year):
    weatherJson = open("weather.json")
    weatherData = json.load(weatherJson)
    try:
        weatherData["weather"][year][month][day]
        return True
    except:
        return False

def getWeather(day, month, year, cityName):
    weatherJson = open("weather.json")
    weatherData = json.load(weatherJson)
    if checkExistsDate(day, month ,year):
        try:
            weather = weatherData["weather"][year][month][day][cityName]
            return weather
        except:
            return False

def getAllCities(day, month, year):
    cityJson = open("city.json")
    cityData = json.load(cityJson)
    weatherJson = open("weather.json")
    weatherData = json.load(weatherJson)

    res = '{"%s %s %s": {' % (month, day, year)
    for city in cityData["cities"].values():
        weather = getWeather(day, month, year, city["cityName"])
        if weather == False: weather = None
        res += '"%s": "%s",' % (city["cityName"], weather)
    res = res[:-1]
    res += '}}'
    return res

def updateWeatherByDate(newData):
    try:
        weatherJson = open("weather.json")
        weatherData = json.load(weatherJson)

        data = json.loads(newData)
        print(data)
        updateDate = list(data.keys())
        updateDate = updateDate[0]
        updateDate = updateDate.split()
        cityList = list(data.values())
        cityList = cityList[0]

        year = updateDate[2]
        month = updateDate[0]
        day = updateDate[1]

        try: weatherData["weather"][year]
        except: weatherData["weather"][year] = {}
        try: weatherData["weather"][year][month]
        except: weatherData["weather"][year][month] = {}

        weatherData["weather"][year][month][day] = cityList
        weatherJson = open("weather.json", "w")
        json.dump(weatherData, weatherJson)

        return True
    except:
        print("Error updating to json file")
        return False

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
                        client.sendall(bytes("SIGN IN: success", "utf8"))
                        print(clientAddr, "SIGN IN: success")
                        return "user"
                    else:
                        client.sendall(bytes("SIGN IN: info incorrect", "utf8"))
                        print(clientAddr, "SIGN IN: info incorrect")
                else:
                    client.sendall(bytes("SIGN IN: syntax error", "utf8"))
                    print(clientAddr, "SIGN IN: syntax error")

            elif reqType == "signup":
                print(clientAddr, "SIGN UP")
                if len(data) == 3:
                    username = data[1]
                    password = data[2]
                    if checkExistUsername(username) == False:
                        createNewUser(username, password)
                        client.sendall(bytes("SIGN UP: success", "utf8"))
                        print(clientAddr, "SIGN UP: success")
                        return True
                    else:
                        client.sendall(bytes("SIGN UP: username already existed", "utf8"))
                        print(clientAddr, "SIGN UP: username already existed")
                else:
                    client.sendall(bytes("SIGN UP: syntax error", "utf8"))
                    print(clientAddr, "SIGN UP: syntax error")

            elif reqType == "signinadmin":
                print(clientAddr, "SIGN IN ADMIN")
                if len(data) == 3:
                    username = data[1]
                    password = data[2]
                    userType = checkLogIn(username, password)
                    if userType == "isAdmin":
                        client.sendall(bytes("SIGN IN ADMIN: success", "utf8"))
                        print(clientAddr, "SIGN IN ADMIN: success")
                        return "admin"
                    else:
                        client.sendall(bytes("SIGN IN ADMIN: info incorrect", "utf8"))
                        print(clientAddr, "SIGN IN ADMIN: info incorrect")
                else:
                    client.sendall(bytes("SIGN IN ADMIN: syntax error", "utf8"))
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
                        client.sendall(bytes("ADMIN ADD CITY: success", "utf8"))
                        print(clientAddr, "ADMIN ADD CITY: success")

                    else:
                        client.sendall(bytes("ADMIN ADD CITY: city already existed", "utf8"))
                        print(clientAddr, "ADMIN ADD CITY: city already existed")

                else:
                    client.sendall(bytes("ADMIN ADD CITY: syntax error", "utf8"))
                    print(clientAddr, "ADMIN ADD CITY: syntax error")

            elif reqType == "choosedate":
                print(clientAddr, "ADMIN CHOOSE DATE: ", data)
                if len(data) == 4:
                    res = getAllCities(data[1], data[2], data[3])
                    if res == False:
                        client.sendall(bytes("ADMIN CHOOSE DATE: Date not found in database", "utf8"))
                        print(clientAddr, "ADMIN CHOOSE DATE: Date not found in database")
                    else:
                        client.sendall(bytes("ADMIN CHOOSE DATE: success\n" + res, "utf8"))
                        print("ADMIN CHOOSE DATE: city list sent successfully")

            elif reqType == "updateddate":
                print(clientAddr, "ADMIN UPDATE BY DATE")
                if len(data) == 2:
                    if updateWeatherByDate(data[1]):
                        client.sendall(bytes("ADMIN UPDATE BY DATE: updated successfully", "utf8"))
                        print("ADMIN UPDATE BY DATE: updated successfully")
                    else:
                        client.sendall(bytes("ADMIN UPDATE BY DATE: error", "utf8"))
                        print("ADMIN UPDATE BY DATE: error")

            elif reqType == "choosecity":
                print(clientAddr, "ADMIN CHOOSE CITY")

            elif reqType == "exit":
                disconnectClient(client, clientAddr)
                return

            else:
                client.sendall(bytes("Unknown command", "utf8"))
                print(clientAddr, "Unknown command")

        else: return False


# main function
if __name__ == "__main__":
    today = date.today()
    DAY = today.strftime("%d")
    MONTH = today.strftime("%B")
    YEAR = today.strftime("%Y")
    MONTHS = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "Setemper", "October", "November", "December"]

    HOST = '127.0.0.1'
    PORT = 65432

    clientAddrs = {}

    weatherJson = open("weather.json")
    cityJson = open("city.json")
    cityData = json.load(cityJson)
    data = json.load(weatherJson)
    userJson = open("user.json")
    userData = json.load(userJson)
    cityData = cityData["cities"]
    weatherData = data["weather"]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("Server 1 is online, wating for connections...")

    acceptClientConnections()
    server.close()
