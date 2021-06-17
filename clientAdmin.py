import socket
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from datetime import date


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
    if (serverResponse == "SIGN IN ADMIN: success"):
        messagebox.showinfo("Success", "You have signed in successfully")
        showFrame(mainMenuFrame)
    elif (serverResponse == "SIGN IN ADMIN: info incorrect"):
        messagebox.showerror("Error", "Incorrect admin username or password")
    elif (serverResponse == "SIGN IN ADMIN: syntax error"):
        messagebox.showerror("Error", "Username or password can't be empty")

    elif (serverResponse == "ADMIN ADD CITY: success"):
        messagebox.showinfo("Success", "You have added a new city successfully")
    elif (serverResponse == "ADMIN ADD CITY: city already existed"):
        messagebox.showerror("Error", "City already existed")
    elif (serverResponse == "ADMIN ADD CITY: syntax error"):
        messagebox.showerror("Error", "City name can't be empty")


def showFrame(frame):
    frame.tkraise()

def setUpChooseSVFrame():
    Label(chooseSVFrame, text="SERVER IP").pack(pady=20)
    Label(chooseSVFrame, text="Input server's IP").pack()
    serverIPEntry = Entry(chooseSVFrame)
    #serverIPEntry.bind("<Return>", (lambda event: connectThread(serverIPEntry)))
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
    Button(mainMenuFrame, text="Update weather data by date", width=25, height=1, command=lambda: showFrame(UWBDFrame)).pack(pady=(0,15))
    Button(mainMenuFrame, text="Update weather data by city", width=25, height=1, command=lambda: showFrame(UWBCFrame)).pack()

def setUpAddCityFrame():
    Button(addCityFrame, text="< Back", width=8, height=1, command=lambda: showFrame(mainMenuFrame)).pack(side=TOP, anchor=NW)
    Label(addCityFrame, text="ADD CITY").pack(pady=20)
    Label(addCityFrame, text="New city name").pack()
    cityNameEntry = Entry(addCityFrame)
    cityNameEntry.pack()

    Button(addCityFrame, text="Add", width=10, height=1, command=lambda: addCityThread(cityNameEntry)).pack(pady=(20,10))

def setUpUWBDFrame():
    Button(UWBDFrame, text="< Back", width=8, height=1, command=lambda: showFrame(mainMenuFrame)).pack(side=TOP, anchor=NW)
    Label(UWBDFrame, text="UPDATE WEATHER DATA BY DATE").pack(pady=20)

    #Day
    dayList = list(range(32))

    Label(UWBDFrame, text = "Choose day").pack()
    dayChoose = StringVar(UWBDFrame)
    dayOption = ttk.Combobox(UWBDFrame, textvariable=dayChoose, values=dayList, width=10)
    dayChoose = dayList.index(DAY)
    dayOption.current(dayChoose)
    dayOption.pack(pady=(0,15))

    #Month
    monthList = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "Setemper", "October", "November", "December"]

    Label(UWBDFrame, text = "Choose Month").pack()
    monthChoose = StringVar(UWBDFrame)
    monthOption = ttk.Combobox(UWBDFrame, textvariable=monthChoose, value=monthList,width=10)
    monthChoose = monthList.index(MONTH)
    monthOption.current(monthChoose)
    monthOption.pack(pady=(0,15))

    #Year
    yearList = ["2020","2021","2022"]

    Label(UWBDFrame, text = "Choose Year").pack()
    yearChoose = StringVar(UWBDFrame)
    yearOption = ttk.Combobox(UWBDFrame, textvariable = yearChoose, values=yearList,width=10)
    yearChoose = yearList.index(YEAR)
    yearOption.current(yearChoose)
    yearOption.pack(pady=(0,20))

    Button(UWBDFrame, text="Choose", width=12, height=1, command=lambda: sendDate(dayOption.get(),monthOption.get(),yearOption.get() )).pack()

def setUpUWBCFrame():
    Button(UWBCFrame, text="< Back", width=8, height=1, command=lambda: showFrame(mainMenuFrame)).pack(side=TOP, anchor=NW)
    Label(UWBCFrame, text="UPDATE WEATHER DATA BY CITY").pack(pady=20)


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
    if(send("addcity " + cityName)):
        serverResponse = receive()
        frameManager(serverResponse)

def sendDateThread(day, month, year):
    threadDate = Thread(target=sendDate, args=(day, month, year,))
    threadDate.daemon = True
    threadDate.start()

def sendDate(day, month, year):
    message = "updatebydate %s %s %s" % (day, month, year)
    if(send(message)):
        serverResponse = receive()
        print(serverResponse)


# main function
if __name__ == "__main__":
    today = date.today()
    DAY = int(today.strftime("%d"))
    MONTH = today.strftime("%B")
    YEAR = today.strftime("%Y")

    PORT = 65432
    root = Tk()
    root.geometry("400x400")
    root.title("Weathery App - Admin")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    chooseSVFrame = Frame(root)
    signInFrame = Frame(root)
    mainMenuFrame = Frame(root)
    addCityFrame = Frame(root)
    UWBDFrame = Frame(root)
    UWBCFrame = Frame(root)

    for frame in (chooseSVFrame, signInFrame, mainMenuFrame, addCityFrame, UWBDFrame, UWBCFrame):
        frame.grid(row=0, column=0, sticky='nsew')

    setUpChooseSVFrame()
    setUpSignInFrame()
    setUpMainMenuFrame()
    setUpAddCityFrame()
    setUpUWBDFrame()
    setUpUWBCFrame()

    Thread(target=showFrame, args=(chooseSVFrame,)).start()

    root.protocol("WM_DELETE_WINDOW", exitApp) # handle when click "X" on tkinter app
    root.mainloop()





