#import libraries
from os import truncate
import socket
import json
from threading import Thread
from tkinter.constants import TRUE


# helper functions
def checkExistUsername(username):
    userJson = open("user.json")
    userData = json.load(userJson)
    for user in userData["users"].values():
        if user["username"] == username:
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

def createNewCity(cityName):
    cityJson = open("city.json")
    cityData = json.load(cityJson)
    newCity= {len(cityData["cities"]): {"cityName": cityName}}
    with open("city.json", "r+") as file:
        fileData = json.load(file)
        fileData["cities"].update(newCity)
        file.seek(0)
        json.dump(fileData, file, indent = 4)

# server functions
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
    clientType = logInSection(client, clientAddr)
    if clientType == "user":
        userSection(client, clientAddr)
    elif clientType == "admin":
        adminSection(client, clientAddr)

def logInSection(client, clientAddr):
    while True:
        data = receiveClientReq(client, clientAddr)
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
        data = receiveClientReq(client, clientAddr)
        if data:
            reqType = data[0]
            if reqType == "exit":
                disconnectClient(client, clientAddr)
                return
        else: return

def adminSection(client, clientAddr):
    while True:
        data = receiveClientReq(client, clientAddr)
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
            elif reqType == "exit":
                disconnectClient(client, clientAddr)
                return

            else:
                client.sendall(bytes("ADMIN ADD CITY: syntax error", "utf8"))
                print(clientAddr, "ADMIN ADD CITY: syntax error")

        else: return False


# main function
if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432

    clientAddrs = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("Server 1 is online, wating for connections...")

    acceptClientConnections()
    server.close()
