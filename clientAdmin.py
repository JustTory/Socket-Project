# NHỚ BỎ SKIP LOGIN TRƯỚC KHI NỘP NHA BROOOOOOOOO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

    elif (serverResponse[0] == "ADMIN UPDATE BY DATE: updated successfully" or serverResponse[0] == "ADMIN UPDATE BY CITY: updated successfully"):
        messagebox.showinfo("Success", "Data updated in database successfully")
    elif (serverResponse[0] == "ADMIN UPDATE BY DATE: error" or serverResponse[0] == "ADMIN UPDATE BY CITY: error"):
        messagebox.showerror("Error", "Something went wrong, can't update data in database")

    elif len(serverResponse) > 1:
        data = json.loads(serverResponse[1])
        if(serverResponse[0] == "ADMIN GET CITY LIST: success"):
            setUpChooseCityFrame(data)
            showFrame(chooseCityFrame)
        elif (serverResponse[0] == "ADMIN CHOOSE DATE: success"):
            setUpUpdateDataFrame(data, "date")
            showFrame(updateDataFrame)
        elif (serverResponse[0] == "ADMIN CHOOSE CITY: success"):
            setUpUpdateDataFrame(data, "city")
            showFrame(updateDataFrame)

def showFrame(frame):
    frame.tkraise()

def back(thisFrame, nextFrame):
    for child in thisFrame.winfo_children():
        child.destroy()
    showFrame(nextFrame)

def selectRow(event, weatherLabel, weatherOption):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        item = event.widget.get(index)
        item = item.split(":")
        name = item[0]
        weather = item[1][1:]
        weatherLabel.configure(text=name + "'s weather")
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

        if listBox.curselection()[0] < listBox.size():
            listBox.delete(ANCHOR)
            listBox.insert(ANCHOR, newItem)
            data[updateData][name] = newWeather
    except:
        messagebox.showerror("Error", "Please select a row to update")

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

    Button(chooseCityFrame, text="Select", width=15, height=1, command=lambda: sendCityThread(cityOption.get())).pack()

def setUpUpdateDataFrame(data, type):
    weatherList = list(data.values())
    weatherList = weatherList[0]
    updateType = list(data.keys())
    updateType = updateType[0]

    if type == "city":
        title = "CITY"
        backFrame = chooseCityFrame
        command = "updatedcity"
    elif type == "date":
        title = "DATE"
        backFrame = chooseDateFrame
        command = "updateddate"

    listBox = Listbox(updateDataFrame, width=30, selectmode=SINGLE, exportselection=False)
    weatherLabel = Label(updateDataFrame, text="Weather value")
    weatherChoose = StringVar(updateDataFrame)
    weatherOption = ttk.Combobox(updateDataFrame, textvariable=weatherChoose,values=weatherType,width=15,justify='center',state="readonly")
    weatherChoose = 0
    weatherOption.current(weatherChoose)
    updateBtn = Button(updateDataFrame, text="Update", width=8, height=1, command=lambda: updateWeather(data, updateType, listBox, weatherOption.get()))
    saveBtn = Button(updateDataFrame, text="Save changes", width=15, height=1, command=lambda: sendUpdatedDataThread(data, command))

    for name in weatherList:
        listBox.insert(END, name + ": " + weatherList[name])

    Button(updateDataFrame, text="< Back", width=8, height=1, command=lambda: back(updateDataFrame, backFrame)).pack(side=TOP, anchor=NW)
    Label(updateDataFrame, text="UPDATE WEATHER DATA BY " + title).pack(pady=20)
    Label(updateDataFrame, text=updateType).pack()
    listBox.pack(pady=(0,10))
    weatherLabel.pack()
    weatherOption.pack(pady=(0,10))
    updateBtn.pack(pady=(0,20))
    saveBtn.pack()

    listBox.bind('<<ListboxSelect>>', lambda event: selectRow(event, weatherLabel, weatherOption))

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
    threadAddCity = Thread(target=addCity, args=(cityNameEntry,))
    threadAddCity.daemon = True
    threadAddCity.start()
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

def getCityList():
    message = "getcitylist"
    if(send(message)):
        serverResponse = receive()
        frameManager(serverResponse)

def sendCityThread(city):
    threadSendCity = Thread(target=sendCity, args=(city,))
    threadSendCity.daemon = True
    threadSendCity.start()
def sendCity(city):
    message = "choosecity\n%s" % (city)
    if(send(message)):
        serverResponse = receive()
        frameManager(serverResponse)

def sendUpdatedDataThread(data, command):
    threadSendCityList = Thread(target=sendUpdatedData, args=(data, command,))
    threadSendCityList.daemon = True
    threadSendCityList.start()
def sendUpdatedData(data, command):
    jsonData = json.dumps(data)
    message = command + "\n" + jsonData
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
    chooseCityFrame = Frame(root)
    updateDataFrame = Frame(root)

    for frame in (chooseSVFrame, signInFrame, mainMenuFrame, addCityFrame, chooseDateFrame, chooseCityFrame, updateDataFrame):
        frame.grid(row=0, column=0, sticky='nsew')

    setUpChooseSVFrame()
    setUpSignInFrame()
    setUpMainMenuFrame()
    setUpAddCityFrame()
    setUpChooseDateFrame()

    Thread(target=showFrame, args=(chooseSVFrame,)).start()

    root.protocol("WM_DELETE_WINDOW", exitApp) # handle when click "X" on tkinter app
    root.mainloop()





