import socket
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from datetime import date
import json

# helper functions
def send(msg):
    try:
        client.sendall(bytes(msg, "utf8"))
        return True
    except:
        print("Server is offline or request timeout")
        messagebox.showerror("Error", "Server is offline or request timeout")
        showFrame(chooseSVFrame)
        return False

def receive():
    msg = client.recv(1024).decode("utf8")
    if len(msg) == 0:
        print("Server has disconnected")
    return msg

def frameManager(serverResponse):
    print(serverResponse)
    serverResponse = serverResponse.split("\n")

    if (serverResponse[0] == "SIGN IN ADMIN: success"):
        showFrame(mainMenuFrame)
        messagebox.showinfo("Success", "You have signed in successfully")
    elif (serverResponse[0] == "SIGN IN ADMIN: info incorrect"):
        messagebox.showerror("Error", "Incorrect admin username or password")
    elif (serverResponse[0] == "SIGN IN ADMIN: syntax error"):
        messagebox.showerror("Error", "Username or password can't be empty")

    elif (serverResponse[0] == "ADMIN ADD CITY: success"):
        messagebox.showinfo("Success", "You have added a new city successfully")
    elif (serverResponse[0] == "ADMIN ADD CITY: city already existed"):
        messagebox.showerror("Error", "City already existed")
    elif (serverResponse[0] == "ADMIN ADD CITY: syntax error"):
        messagebox.showerror("Error", "City name can't be empty")

    elif (serverResponse[0] == "ADMIN CHOOSE DATE: Date not found in database"):
        messagebox.showerror("Error", "Date not found in database")
    elif (serverResponse[0] == "ADMIN UPDATE BY DATE: updated successfully" or serverResponse[0] == "ADMIN UPDATE BY CITY: updated successfully"):
        messagebox.showinfo("Success", "Data updated in database successfully")
    elif (serverResponse[0] == "ADMIN UPDATE BY DATE: error" or serverResponse[0] == "ADMIN UPDATE BY CITY: error"):
        messagebox.showerror("Error", "Something went wrong, can't update data in database")

    elif len(serverResponse) > 1:
        data = json.loads(serverResponse[1])
        if (serverResponse[0] == "ADMIN CHOOSE DATE: success"):
            setUpUWBDFrame(data)
            showFrame(UWBDFrame)
        elif(serverResponse[0] == "ADMIN GET CITY LIST: success"):
            setUpChooseCityFrame(data)
            showFrame(chooseCityFrame)
        elif(serverResponse[0] == "ADMIN CHOOSE CITY: success"):
            setUpUWBCFrame(data)
            showFrame(UWBCFrame)

def showFrame(frame):
    frame.tkraise()

def back(thisFrame, nextFrame):
    for child in thisFrame.winfo_children():
        child.destroy()
    showFrame(nextFrame)

def selectCity(event, weatherLabel, weatherEntry):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        item = event.widget.get(index)
        item = item.split(":")
        cityName = item[0]
        weather = item[1][1:]
        weatherLabel.configure(text=cityName + "'s weather")
        weatherEntry.delete(0, "end")
        weatherEntry.insert(0, weather)

def selectDate(event, weatherLabel, weatherOption):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        item = event.widget.get(index)
        item = item.split(":")
        date = item[0]
        weather = item[1][1:]
        weatherLabel.configure(text=date + "'s weather")
        pos = 0
        for i in weatherType:
            if i == weather:
                break
            pos = pos + 1
        if pos <= 5: weatherOption.current(pos)
        else: weatherOption.current(0)

def updateWeather(data, updateData, listBox, newWeather):
    try:
        oldItem = listBox.get(ANCHOR)
        oldItem = oldItem.split(":")
        name = oldItem[0]
        newItem = name + ": " + newWeather
        listBox.delete(ANCHOR)
        listBox.insert(ANCHOR, newItem)
        data[updateData][name] = newWeather
    except:
        print("end of list")

# frame funtions
def setUpChooseSVFrame():
    Label(chooseSVFrame, text="SERVER IP").pack(pady=20)
    Label(chooseSVFrame, text="Input server's IP").pack()
    serverIPEntry = Entry(chooseSVFrame, width=20)
    serverIPEntry.pack()
    serverIPEntry.focus()

    Button(chooseSVFrame, text="Connect", height="1", width="10", command=lambda:connectThread(serverIPEntry)).pack(pady=10)

def setUpSignInFrame():
    Button(signInFrame, text="< Disconnect", width=10, height=1, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(signInFrame, text="SIGN IN").pack(pady=20)
    Label(signInFrame, text="Admin username").pack()
    usernameEntry = Entry(signInFrame)
    #usernameEntry.bind("<Return>", (lambda event: sendUserInfoThread(usernameEntry, passwordEntry, "signinadmin")))
    usernameEntry.pack()

    Label(signInFrame, text="Admin password").pack(pady=(10,0))
    passwordEntry = Entry(signInFrame, show= '*')
    #passwordEntry.bind("<Return>", (lambda event: sendUserInfoThread(usernameEntry, passwordEntry, "signinadmin")))
    passwordEntry.pack()

    Button(signInFrame, text="Login", width=10, height=1, command=lambda: sendUserInfoThread(usernameEntry, passwordEntry, "signinadmin")).pack(pady=(20,10))

def setUpMainMenuFrame():
    Button(mainMenuFrame, text="< Disconnect", width=10, height=1, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(mainMenuFrame, text="MAIN MENU").pack(pady=20)
    Button(mainMenuFrame, text="Add new city", width=15, height=1, command=lambda: showFrame(addCityFrame)).pack(pady=(0,15))
    Button(mainMenuFrame, text="Update weather data by date", width=25, height=1, command=lambda: showFrame(chooseDateFrame)).pack(pady=(0,15))
    Button(mainMenuFrame, text="Update weather data by city", width=25, height=1, command=lambda: getCityList()).pack()

def setUpAddCityFrame():
    Button(addCityFrame, text="< Back", width=8, height=1, command=lambda: showFrame(mainMenuFrame)).pack(side=TOP, anchor=NW)
    Label(addCityFrame, text="ADD CITY").pack(pady=20)
    Label(addCityFrame, text="New city name").pack()
    cityNameEntry = Entry(addCityFrame)
    cityNameEntry.pack()

    Button(addCityFrame, text="Add", width=10, height=1, command=lambda: addCityThread(cityNameEntry)).pack(pady=(20,10))

def setUpChooseDateFrame():
    Button(chooseDateFrame, text="< Back", width=8, height=1, command=lambda: showFrame(mainMenuFrame)).pack(side=TOP, anchor=NW)
    Label(chooseDateFrame, text="CHOOSE DATE").pack(pady=20)

    #Day
    dayList = list(range(32))

    Label(chooseDateFrame, text = "Choose day").pack()
    dayChoose = StringVar(chooseDateFrame)
    dayOption = ttk.Combobox(chooseDateFrame, textvariable=dayChoose, values=dayList, width=10,justify='center',state="readonly")
    dayChoose = dayList.index(DAY)
    dayOption.current(dayChoose)
    dayOption.pack(pady=(0,15))

    #Month
    monthList = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "Setemper", "October", "November", "December"]

    Label(chooseDateFrame, text = "Choose Month").pack()
    monthChoose = StringVar(chooseDateFrame)
    monthOption = ttk.Combobox(chooseDateFrame, textvariable=monthChoose, value=monthList,width=10,justify='center',state="readonly")
    monthChoose = monthList.index(MONTH)
    monthOption.current(monthChoose)
    monthOption.pack(pady=(0,15))

    #Year
    yearList = ["2020","2021","2022"]

    Label(chooseDateFrame, text = "Choose Year").pack()
    yearChoose = StringVar(chooseDateFrame)
    yearOption = ttk.Combobox(chooseDateFrame, textvariable = yearChoose, values=yearList,width=10,justify='center',state="readonly")
    yearChoose = yearList.index(YEAR)
    yearOption.current(yearChoose)
    yearOption.pack(pady=(0,20))

    Button(chooseDateFrame, text="Choose", width=12, height=1, command=lambda: sendDateThread(dayOption.get(),monthOption.get(),yearOption.get() )).pack()

def setUpUWBDFrame(data):
    cityList = list(data.values())
    cityList = cityList[0]

    updateDate = list(data.keys())
    updateDate = updateDate[0]

    listBox = Listbox(UWBDFrame, width=30, selectmode=SINGLE, exportselection=False)
    weatherLabel = Label(UWBDFrame, text="Weather value")
    weatherEntry = Entry(UWBDFrame)
    updateBtn = Button(UWBDFrame, text="Update", width=8, height=1, command=lambda: updateWeather(data, updateDate, listBox, weatherEntry.get()))
    saveBtn = Button(UWBDFrame, text="Save changes", width=15, height=1, command=lambda: sendCityListThread(data))

    for city in cityList:
        listBox.insert(END, city + ": " + cityList[city])

    Button(UWBDFrame, text="< Back", width=8, height=1, command=lambda: back(UWBDFrame, chooseDateFrame)).pack(side=TOP, anchor=NW)
    Label(UWBDFrame, text="UPDATE WEATHER DATA").pack(pady=20)
    Label(UWBDFrame, text=updateDate).pack()
    listBox.pack(pady=(0,10))
    weatherLabel.pack()
    weatherEntry.pack(pady=(0,10))
    updateBtn.pack(pady=(0,20))
    saveBtn.pack()

    listBox.bind('<<ListboxSelect>>', lambda event: selectCity(event, weatherLabel, weatherEntry))

def setUpChooseCityFrame(data):
    cityList = list(data.values())

    Button(chooseCityFrame, text="< Back", width=8, height=1, command=lambda: back(chooseCityFrame, mainMenuFrame)).pack(side=TOP, anchor=NW)
    Label(chooseCityFrame, text = "CHOOSE CITY").pack(pady=20)
    cityChoose = StringVar(chooseCityFrame)
    cityOption = ttk.Combobox(chooseCityFrame, textvariable=cityChoose,values=cityList,width=20,justify='center',state="readonly")
    cityChoose = 0
    cityOption.current(cityChoose)
    cityOption.pack()

    cityLabel = Label(chooseCityFrame, text="")
    cityLabel.pack()

    Button(chooseCityFrame, text="Select", width=15, height=1, command=lambda: sendCity(cityOption.get())).pack()

def setUpUWBCFrame(data):
    weatherList = list(data.values())
    weatherList = weatherList[0]

    updateCity = list(data.keys())
    updateCity = updateCity[0]

    listBox = Listbox(UWBCFrame, width=30, selectmode=SINGLE, exportselection=False)
    weatherLabel = Label(UWBCFrame, text="Weather value")
    weatherChoose = StringVar(UWBCFrame)
    weatherOption = ttk.Combobox(UWBCFrame, textvariable=weatherChoose,values=weatherType,width=15,justify='center',state="readonly")
    weatherChoose = 0
    weatherOption.current(weatherChoose )
    updateBtn = Button(UWBCFrame, text="Update", width=8, height=1, command=lambda: updateWeather(data, updateCity, listBox, weatherOption.get()))

    saveBtn = Button(UWBCFrame, text="Save changes", width=15, height=1, command=lambda: sendDateList(data))

    for weather in weatherList:
        listBox.insert(END, weather + ": " + weatherList[weather])

    Button(UWBCFrame, text="< Back", width=8, height=1, command=lambda: back(UWBCFrame, chooseCityFrame)).pack(side=TOP, anchor=NW)
    Label(UWBCFrame, text="UPDATE WEATHER DATA BY CITY").pack(pady=20)
    Label(UWBCFrame, text=updateCity).pack()
    listBox.pack(pady=(0,10))
    weatherLabel.pack()
    weatherOption.pack(pady=(0,10))
    updateBtn.pack(pady=(0,20))
    saveBtn.pack()

    listBox.bind('<<ListboxSelect>>', lambda event: selectDate(event, weatherLabel, weatherOption))

# client functions
def disconnectThread():
    threadDisconnect = Thread(target=disconnectServer)
    threadDisconnect.daemon = True
    threadDisconnect.start()
def disconnectServer():
    send("exit")
    client.close()
    print("disconnected from server")
    showFrame(chooseSVFrame)

def exitApp():
    try:
        client
        send("exit")
        client.close()
    except NameError:
        print("closing app")
    root.destroy()

def connectThread(entry):
    threadConnect = Thread(target=connectServer, args=(entry,))
    threadConnect.daemon = True
    threadConnect.start()
def connectServer(entry):
    global client # client socket
    host = entry.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddr = ("localhost", PORT)
    try:
        client.connect(serverAddr)
        print('Connected to server: ' + str(serverAddr))
        showFrame(signInFrame)
    except:
        print("Could not find server's IP or request timeout")
        messagebox.showerror("Error", "Could not find server's IP or request timeout")

def sendUserInfoThread(usernameEntry, passwordEntry, type):
    threadSend = Thread(target=sendUserInfo, args=(usernameEntry, passwordEntry, type,))
    threadSend.daemon = True
    threadSend.start()
def sendUserInfo(usernameEntry, passwordEntry, type):
    username = usernameEntry.get()
    usernameEntry.delete(0, 'end')
    password = passwordEntry.get()
    passwordEntry.delete(0, 'end')

    if(send(type + " " + "admin" + " " + "admin")):
        serverResponse = receive()
        frameManager(serverResponse)

def addCityThread(cityNameEntry):
    threadCity = Thread(target=addCity, args=(cityNameEntry,))
    threadCity.daemon = True
    threadCity.start()
def addCity(cityNameEntry):
    cityName = cityNameEntry.get()
    cityNameEntry.delete(0, 'end')
    if(send("addcity\n" + cityName)):
        serverResponse = receive()
        frameManager(serverResponse)

def sendDateThread(day, month, year):
    threadDate = Thread(target=sendDate, args=(day, month, year,))
    threadDate.daemon = True
    threadDate.start()
def sendDate(day, month, year):
    message = "choosedate\n%s\n%s\n%s" % (day, month, year)
    if(send(message)):
        serverResponse = receive()
        frameManager(serverResponse)

def sendCityListThread(data):
    threadSendCityList = Thread(target=sendCityList, args=(data,))
    threadSendCityList.daemon = True
    threadSendCityList.start()
def sendCityList(data):
    jsonData = json.dumps(data)
    message = "updateddate\n" + jsonData
    if(send(message)):
        serverResponse = receive()
        frameManager(serverResponse)

def getCityList():
    message = "getcitylist"
    if(send(message)):
        serverResponse = receive()
        frameManager(serverResponse)

def sendCity(city):
    message = "choosecity\n%s" % (city)
    if(send(message)):
        serverResponse = receive()
        frameManager(serverResponse)

def sendDateList(data):
    jsonData = json.dumps(data)
    message = "updatedcity\n" + jsonData
    if(send(message)):
        serverResponse = receive()
        frameManager(serverResponse)

# main function
if __name__ == "__main__":
    today = date.today()
    DAY = int(today.strftime("%d"))
    MONTH = today.strftime("%B")
    YEAR = today.strftime("%Y")

    weatherType = ['null', 'Rainy', 'Sunny', 'Cloudy', 'Windy', 'Snowy']

    PORT = 65432
    root = Tk()
    root.geometry("500x500")
    root.title("Weathery App - Admin")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    chooseSVFrame = Frame(root)
    signInFrame = Frame(root)
    mainMenuFrame = Frame(root)
    addCityFrame = Frame(root)
    chooseDateFrame = Frame(root)
    UWBDFrame = Frame(root)
    chooseCityFrame = Frame(root)
    UWBCFrame = Frame(root)

    for frame in (chooseSVFrame, signInFrame, mainMenuFrame, addCityFrame, chooseDateFrame, UWBDFrame, chooseCityFrame, UWBCFrame):
        frame.grid(row=0, column=0, sticky='nsew')

    setUpChooseSVFrame()
    setUpSignInFrame()
    setUpMainMenuFrame()
    setUpAddCityFrame()
    setUpChooseDateFrame()

    Thread(target=showFrame, args=(chooseSVFrame,)).start()

    root.protocol("WM_DELETE_WINDOW", exitApp) # handle when click "X" on tkinter app
    root.mainloop()





