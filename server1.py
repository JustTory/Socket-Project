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
    print("logInSection")
    errorMsg = ""
    while True:
        print("log in")
        loginHint = errorMsg + "Type /signin to sign in or /signup to create a new account"
        conn.sendall(bytes(loginHint, "utf8"))
        clientInput = conn.recv(1024)
        strClientInput = clientInput.decode("utf8")
        if strClientInput == "/signin":
            errorMsg = ""
            while True:
                print("sign in")
                loginReq = errorMsg + "Sign In: type [username] [password]"
                conn.sendall(bytes(loginReq, "utf8"))
                clientInput = conn.recv(1024)
                strClientInput = clientInput.decode("utf8")
                userInfo = strClientInput.split()
                if len(userInfo) == 2:
                    username = userInfo[0]
                    password = userInfo[1]
                else:
                    errorMsg = "\nSyntax error!\n"
                    continue
                if checkLogIn(username, password, userData):
                    conn.sendall(bytes("You have signed in successfully!", "utf8"))
                    break
                else:
                    errorMsg = "\nIncorrect username or password!\n"
            break
        elif strClientInput == "/signup":
            errorMsg = ""
            while True:
                print("sign up")
                loginReq = errorMsg + "Sign Up: type [username] [password]"
                conn.sendall(bytes(loginReq, "utf8"))
                clientInput = conn.recv(1024)
                strClientInput = clientInput.decode("utf8")
                userInfo = strClientInput.split()
                if len(userInfo) == 2:
                    username = userInfo[0]
                    password = userInfo[1]
                else:
                    errorMsg = "\nSyntax error!\n"
                    continue
                if checkExistUsername(username, userData) == False:
                    createNewUser(username, password, userData)
                    conn.sendall(bytes("You have created a new account successfully", "utf8"))
                    break
                else:
                    errorMsg = "\nUsername already exists!\n"
            break
        else:
            print("unknown command")
            errorMsg = "\nUnknown command!\n"

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


def communicateSection(conn, weatherData):
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

        logInSection(conn, userData)
        communicateSection(conn, weatherData)

        conn.close()
        print(addr, "has disconnected")

    s.close()
