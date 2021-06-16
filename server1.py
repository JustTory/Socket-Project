#import libraries
import socket
import json
from threading import Thread


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

def commandManager(strClientReq, weatherData):
    commandArr = strClientReq.split()
    if commandArr[0] == "/help":
        return "\n/city [city_name]\n[city_name]: TPHCM, HaNoi, DaNang, Hue"
    elif commandArr[0] == "/city":
        for city in weatherData["cities"]:
            if city['cityName'] == commandArr[1]:
                res = "\n"
                for days in city["data"]:
                    res += "%s: %s\n" % (days, city["data"][days])
                return res
        return "City name not found!"
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
    # hint = "logged in"
    # client.sendall(bytes(hint, "utf8"))

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
    weatherData = json.load(weatherJson)
    userJson = open("user.json")
    userData = json.load(userJson)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("Server 1 is online, wating for connections...")

    threadAccept = Thread(target=acceptClientConnections)
    threadAccept.start()
    threadAccept.join()
    server.close()
