#import libraries
import socket
import json


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

def logInSection(conn, userData):
    while True:
        clientReq = conn.recv(1024)
        strclientReq = clientReq.decode("utf8")
        data = strclientReq.split()
        reqType = data[0]

        if reqType == "signin":
            print("signin")
            if len(data) == 3:
                username = data[1]
                password = data[2]
                if checkLogIn(username, password, userData):
                    conn.sendall(bytes("sign in success", "utf8"))
                    print("sign in success")
                    break
                else:
                    conn.sendall(bytes("info incorrect", "utf8"))
                    print("info incorrect")
            else:
                conn.sendall(bytes("syntax error", "utf8"))
                print("syntax error")

        elif reqType == "signup":
            print("signup")
            if len(data) == 3:
                username = data[1]
                password = data[2]
                if checkExistUsername(username, userData) == False:
                    createNewUser(username, password, userData)
                    conn.sendall(bytes("sign up success", "utf8"))
                    print("sign up success")
                    break
                else:
                    conn.sendall(bytes("username exists", "utf8"))
                    print("username exists")
            else:
                conn.sendall(bytes("syntax error", "utf8"))
                print("syntax error")

        else:
            conn.sendall(bytes("unknown command", "utf8"))
            print("unknown command")

def commandManager(strclientReq, weatherData):
    commandArr = strclientReq.split()
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


def communicateSection(conn, weatherData):
    hint = "logged in"
    conn.sendall(bytes(hint, "utf8"))

    while True:
        clientReq = conn.recv(1024)
        strclientReq = clientReq.decode("utf8")

        if strclientReq == "/exit":
            break
        if not clientReq:
            break

        print(addr, strclientReq)
        serverResponse = commandManager(strclientReq, weatherData)
        conn.sendall(bytes(serverResponse, "utf8"))


# main function
if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432

    weatherJson = open("weather.json")
    weatherData = json.load(weatherJson)
    userJson = open("user.json")
    userData = json.load(userJson)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print("Server 1 is online, wating for connections...")

    while True:
        conn, addr = s.accept()
        print(addr, "has connected")

        logInSection(conn, userData)
        communicateSection(conn, weatherData)

        conn.close()
        print(addr, "has disconnected")

    s.close()
