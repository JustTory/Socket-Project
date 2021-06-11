#import libraries
import socket
import json


# helper functions
def commandManager(strClientInput, weatherData):
    commandArr = strClientInput.split()
    if commandArr[0] == "/help":
        return "\n/city [city_name]\n[city_name]: TPHCM, HaNoi, DaNang, Hue"
    elif commandArr[0] == "/city":
        for city in weatherData["cities"]:
            if city['cityName'] == commandArr[1]:
                res = "\n"
                for days in city['data']:
                    res += "%s: %s\n" % (days, city['data'][days])
                return res;
        return "City name not found!"
    else: return "Unknown command!"


# main function
if __name__ == "__main__":
    HOST = '127.0.0.1' # server's IP
    PORT = 65432 # server's port: any non-privileged ports

    weatherJson = open('weather.json') # open json file
    weatherData = json.load(weatherJson) #load json data to an array

    # s = socket.socket(addr_family, type)
    # addr_family:
    #   socket.AF_INET: Internet protocol (IPv4)
    #   socket.AF_INET6: Internet protocol (IPv6)
    # type:
    #   socket.SOCK_STREAM: Connection based stream (TCP)
    #   socket.SOCK_DGRAM: Datagrams (UDP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print("Server 1 is online, wating for connections...")

    while True:
        conn, addr = s.accept()
        print(addr, "has connected")

        while True:
            clientInput = conn.recv(1024)
            strClientInput = clientInput.decode("utf8")

            if strClientInput == "/exit": break
            if not clientInput: break

            print(addr, strClientInput)
            serverResponse = commandManager(strClientInput, weatherData)
            conn.sendall(bytes(serverResponse, "utf8"))

        conn.close()
        print(addr, "has disconnected")

    s.close()

