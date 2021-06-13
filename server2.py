import socket
import json
from datetime import date

today = date.today()

DAY = today.strftime("%d")
MONTH = today.strftime("%B")

print(DAY)
print(MONTH)

HOST = '127.0.0.1' # server's IP
PORT = 65432 # server's port: any non-privileged ports
weatherJson = open("weather.json")
weatherData = json.load(weatherJson)

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
print("Server 2 is online, wating for connections...")

while True:
    conn, addr = s.accept()
    print(addr, "has connected")

    while True:
        data = conn.recv(1024)
        str_data = data.decode("utf8")

        if str_data == "exit": break
        if not data: break


        print("Client: " + str_data)
        res = "NaN data"
        user_req = str_data.split()
        if (user_req[0] == "/city"):
            print("run in here 1")
            for city in weatherData["cities"]:
                print("run in here 2")
                if (city["cityName"] == user_req[1]):
                    print("run in here 3")
                    res = "\n"
                    for days in range (int(DAY) - 6,int(DAY) + 1):
                        res += "%s %s: %s\n" % (MONTH,days, city["data"][MONTH][str(days)])
                    break

        conn.sendall(bytes(res, "utf8"))

    conn.close()
    print(addr, "has disconnected")

s.close()