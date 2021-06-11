#import libraries
import socket
import json


# functions
def checkExistUsername(username, userData):
    for user in userData["users"]:
        if user["username"] == username:
            return False
    return True

def createNewUser(username, password, userData):
    if checkExistUsername(username, userData) == False:
        newUser = {
            "userID": len(userData["users"]),
            "username": username,
            "password": password
        }
        userData["users"].append(newUser)
        return True
    else:
        return False

def checkLogIn(username, password, userData):
    for user in userData["users"]:
        if user["username"] == username and user["password"] == password:
            return user["userID"];
    return False;

def logInSection():
    while True:
        login = "Type /signin to sign in or /signup to create a new account"
        conn.sendall(bytes(login, "utf8"))
        clientInput = conn.recv(1024)
        strClientInput = clientInput.decode("utf8")
        ###continue code


def commandManager(strClientInput, weatherData):
    commandArr = strClientInput.split()
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
        return "Unknown command!"


def communicateSection():
    hint = "Server: type /help for list of commands"
    conn.sendall(bytes(hint, "utf8"))

    while True:
        clientInput = conn.recv(1024)
        strClientInput = clientInput.decode("utf8")

        if strClientInput == "/exit":
            break
        if not clientInput:
            break

        print(addr, strClientInput)
        serverResponse = commandManager(strClientInput, weatherData)
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

        # functions here

        conn.close()
        print(addr, "has disconnected")

    s.close()
