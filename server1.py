#import libraries
import socket
import json
from threading import Thread
from datetime import date

today = date.today()
# DAY = "13"
DAY = today.strftime("%d")
MONTH = today.strftime("%B")
YEAR = today.strftime("%Y")
MONTHS = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "Setemper", "October", "November", "December"]
# functions
def checkExistUsername(username, userData):
    for user in userData["users"]:
        if user["username"] == username:
            return True
    return False

def createNewUser(username, password, userData):
    newUser = {
        "userID": len(userData["users"]),
        "username": username,
        "password": password
    }

    userData["users"].append(newUser)
    with open("user.json", "w") as outfile:
        json.dump(userData, outfile)

def checkLogIn(username, password, userData):
    for user in userData["users"]:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def logInSection(client, userData):
    while True:
        clientReq = client.recv(1024)
        strclientReq = clientReq.decode("utf8")
        data = strclientReq.split()
        reqType = data[0]

        if reqType == "signin":
            print("signin")
            if len(data) == 3:
                username = data[1]
                password = data[2]
                if checkLogIn(username, password, userData):
                    client.sendall(bytes("sign in success", "utf8"))
                    print("sign in success")
                    break
                else:
                    client.sendall(bytes("info incorrect", "utf8"))
                    print("info incorrect")
            else:
                client.sendall(bytes("syntax error", "utf8"))
                print("syntax error")

        elif reqType == "signup":
            print("signup")
            if len(data) == 3:
                username = data[1]
                password = data[2]
                if checkExistUsername(username, userData) == False:
                    createNewUser(username, password, userData)
                    client.sendall(bytes("sign up success", "utf8"))
                    print("sign up success")
                    break
                else:
                    client.sendall(bytes("username exists", "utf8"))
                    print("username exists")
            else:
                client.sendall(bytes("syntax error", "utf8"))
                print("syntax error")

        else:
            client.sendall(bytes("unknown command", "utf8"))
            print("unknown command")

def getWeatherByCity(city,numDay):
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

def getWeatherByDate(day , month, year):
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
def commandManager(strClientReq, weatherData):
    commandArr = strClientReq.split()
    print(strClientReq)
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

def acceptClientConnections():
    while True:
        client, clientAddr = server.accept()
        print(clientAddr, "has connected")
        clientAddrs[client] = clientAddr
        Thread(target=processClientReq, args=(client, clientAddr,)).start()

def receiveClientReq(client, clientAddr):
    try:
        clientReq = client.recv(1024)
        strclientReq = clientReq.decode("utf8")
        data = strclientReq.split()
        return data
    except:
        disconnectClient(client, clientAddr)
        return False

def disconnectClient(client, clientAddr):
    print(clientAddr, "has disconnected")
    client.close()
    del clientAddrs[client]

def processClientReq(client, clientAddr):
    if(logInSection(client, clientAddr, userData)):
        communicateSection(client, clientAddr, weatherData)


def logInSection(client, clientAddr, userData):
    while True:
        data = receiveClientReq(client, clientAddr)
        if data:
            reqType = data[0]
            if reqType == "signin":
                print(clientAddr ,"SIGN IN")
                if len(data) == 3:
                    username = data[1]
                    password = data[2]
                    if checkLogIn(username, password, userData):
                        client.sendall(bytes("SIGN IN: success", "utf8"))
                        print(clientAddr, "SIGN IN: success")
                        return True
                    else:
                        client.sendall(bytes("SIGN IN: info incorrect", "utf8"))
                        print(clientAddr, "SIGN IN: info incorrect")
                else:
                    client.sendall(bytes("SIGN IN: syntax error", "utf8"))
                    print(clientAddr, "SIGN IN: syntax error")

            elif reqType == "signup":
                print("signup")
                if len(data) == 3:
                    username = data[1]
                    password = data[2]
                    if checkExistUsername(username, userData) == False:
                        createNewUser(username, password, userData)
                        client.sendall(bytes("SIGN UP: success", "utf8"))
                        print(clientAddr, "SIGN UP: success")
                        return True
                    else:
                        client.sendall(bytes("SIGN UP: username already existed", "utf8"))
                        print(clientAddr, "SIGN UP: username already existed")
                else:
                    client.sendall(bytes("SIGN UP: syntax error", "utf8"))
                    print(clientAddr, "SIGN UP: syntax error")

            elif reqType == "exit":
                disconnectClient(client, clientAddr)
                return False

            else:
                client.sendall(bytes("unknown command", "utf8"))
                print(clientAddr, "unknown command")
        else: return False

def communicateSection(client, clientAddr, weatherData):
    while True:
        data = receiveClientReq(client, clientAddr)
        if data:
            reqType = data[0]

            if reqType == "exit":
                disconnectClient(client, clientAddr)
                return

            clientReq = client.recv(1024)
            strclientReq = clientReq.decode("utf8")

            if strclientReq == "/exit":
                break
            if not clientReq:
                break

            serverResponse = commandManager(strclientReq, weatherData)
            client.sendall(bytes(serverResponse, "utf8"))

        else: return


# main function
if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432

    clientAddrs = {}

    weatherJson = open("weather.json")
    cityJson = open("cities.json")
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

    threadAccept = Thread(target=acceptClientConnections)
    threadAccept.start()
    threadAccept.join()
    server.close()
