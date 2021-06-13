import socket
import json
from datetime import date

MONTHS = ["January", "Febuary", "May", "June"]
today = date.today()

DAY = "13"
# DAY = today.strftime("%d")
MONTH = today.strftime("%B")
YEAR = today.strftime("%Y")

print(DAY)
print(MONTH)

HOST = '127.0.0.1' # server's IP
PORT = 65432 # server's port: any non-privileged ports
weatherJson = open("weather.json")
data = json.load(weatherJson)

cityData = data["cities"]
weatherData = data["weather"]

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

def checkExistsCity(id):
    try:
        cityData[id]
    except:
        return False
    return True

def getCityWeather(city, numDay):
    if (checkExistsCity(city) == False):  
        return "This city doesn't exist"

    res = "\n"
    day_loop = DAY
    month_loop = MONTH
    year_loop = YEAR

    if (int(DAY) - 6 < 0): 
        index = MONTHS.index(MONTH)
        PrevMonth = MONTHS[index-1] 
        keys = list(weatherData[YEAR][PrevMonth])
        lastDayofPrevMonth = keys[-1]

    getNumofDay = numDay    
    for i in range(getNumofDay):
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
def getWeatherAll(day = DAY, month = MONTH, year = YEAR): 
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
            data_transfer = getCityWeather(user_req[1], 7)
        if (user_req[0] == "/list"):
            data_transfer = getWeatherAll()

        conn.sendall(bytes(data_transfer, "utf8"))

    conn.close()
    print(addr, "has disconnected")

s.close()