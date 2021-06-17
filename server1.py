#import libraries
import socket
import json
from threading import Thread
from datetime import date

# functions
def checkExistUsername(username, userData):
    for user in userData["users"]:
        if user["username"] == username:
            return True
    return False

def createNewUser(username, password, userData):
    print(userData)
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

def getWeatherAll(day , month, year):
    allCity = list(cityData)

    try:
        date_data = weatherData[year][month][day]
    except:
        return "No data available"
    res = "\n[%s %s, %s]:\n" % (month, day, year)
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
        data_transfer = getWeatherAll(commandArr[1], commandArr[2], commandArr[3])
        return data_transfer
    else:
        return "unknown command"

def communicateSection(client, weatherData):
    # hint = "logged in"
    # client.sendall(bytes(hint, "utf8"))

    print("run here 1")
    while True:
        clientReq = client.recv(1024)
        strclientReq = clientReq.decode("utf8")

        if strclientReq == "/exit":
            break
        if not clientReq:
            break

        serverResponse = commandManager(strclientReq, weatherData)
        print("server Response: ", serverResponse)
        client.sendall(bytes(serverResponse, "utf8"))

def processClientReq(client, clientAddr):
    while True:
        logInSection(client, userData)
        communicateSection(client, weatherData)

        client.close()
        print(clientAddr, "has disconnected")

def acceptClientConnections():
    while True:
        client, clientAddr = server.accept()
        print(clientAddr, "has connected")
        clientAdrrs[client] = clientAddr
        Thread(target=processClientReq, args=(client, clientAddr,)).start()




# main function
if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432

    MONTHS = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "Setemper", "October", "November", "December"]
    today = date.today()

    # DAY = "13"
    DAY = today.strftime("%d")
    MONTH = today.strftime("%B")
    YEAR = today.strftime("%Y")

    clientSockets = {}
    clientAdrrs = {}

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
