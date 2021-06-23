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
    if (serverResponse == "SIGN IN: success"):
        showFrame(mainMenuFrame)
        messagebox.showinfo("Success", "You have signed in successfully")
    elif (serverResponse == "SIGN IN: info incorrect"):
        messagebox.showerror("Error", "Incorrect username or password")
    elif (serverResponse == "SIGN IN: syntax error"):
        messagebox.showerror("Error", "Username or password can't be empty")

    elif (serverResponse == "SIGN UP: success"):
        messagebox.showinfo("Success", "You have created an account successfully")
        showFrame(mainMenuFrame)
    elif (serverResponse == "SIGN UP: username already existed"):
        messagebox.showerror("Error", "Username already exists")
    elif (serverResponse == "SIGN UP: syntax error"):
        messagebox.showerror("Error", "Username or password can't be empty")

def showFrame(frame):
    frame.tkraise()

# frame functions
def setUpChooseSVFrame():
    Label(chooseSVFrame, text="SERVER IP").pack(pady=20)
    Label(chooseSVFrame, text="Input server's IP").pack()
    serverIPEntry = Entry(chooseSVFrame)
    serverIPEntry.pack()
    serverIPEntry.focus()

    Button(chooseSVFrame, text="Connect", height="1", width="10", command=lambda:connectThread(serverIPEntry)).pack(pady=10)

def setUpSignInFrame():
    Button(signInFrame, text="< Disconnect", width=10, height=1, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(signInFrame, text="SIGN IN").pack(pady=20)
    Label(signInFrame, text="Username").pack()
    usernameEntry = Entry(signInFrame)
    usernameEntry.pack()

    Label(signInFrame, text="Password").pack(pady=(10,0))
    passwordEntry = Entry(signInFrame, show= '*')
    passwordEntry.pack()


    Button(signInFrame, text="Login", width=10, height=1, command=lambda: sendUserInfoThread(usernameEntry, passwordEntry, "signin")).pack(pady=(20,10))
    Button(signInFrame, text="Don't have an account? Sign up", width=30, height=1, command=lambda: showFrame(signUpFrame)).pack()

def setUpSignUpFrame():
    Button(signUpFrame, text="< Disconnect", width=10, height=1, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(signUpFrame, text="CREATE ACCOUNT").pack(pady=20)
    Label(signUpFrame, text="Username").pack()
    usernameEntry = Entry(signUpFrame)
    usernameEntry.pack()

    Label(signUpFrame, text="Password").pack(pady=(10,0))
    passwordEntry = Entry(signUpFrame, show= '*')
    passwordEntry.pack()

    Button(signUpFrame, text="Create account", width=15, height=1, command=lambda: sendUserInfoThread(usernameEntry, passwordEntry, "signup")).pack(pady=(20,10))
    Button(signUpFrame, text="Already have an account? Sign in", width=30, height=1, command=lambda: showFrame(signInFrame)).pack()

def setUpMainMenuFrame():
    Button(mainMenuFrame, text="< Disconnect", width=10, height=1, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(mainMenuFrame, text="MAIN MENU").pack(pady=20)
    Button(mainMenuFrame, text="List all cities", width=15, height=1, command=lambda: showFrame(weatherDate)).pack()
    Button(mainMenuFrame, text="Select a city", width=15, height=1, command=lambda: getAllCity()).pack()

def getAllCity():
    # get City JSON
    send("/getCity")
    global cityList 
    cityList = receive()
    cityList = cityList.split("\n")

    showWeatherByCity()
    showFrame(weatherCity)
def showWeatherByCity():
    Button(weatherCity, text="< Back", width=8, height=1, command=lambda: back(weatherCity, mainMenuFrame)).grid(row = 0, column=0)
    Label(weatherCity, text = "CITY DATA").grid(row=0,column=1,sticky="WE",pady=20)


    Label(weatherCity, text = "Choose a city").grid(pady=5,row=1, column=0, sticky="W", padx=(30,5))
    cityChoose = StringVar(weatherCity)
    cityOption = ttk.Combobox(weatherCity, textvariable=cityChoose,values=cityList,width=15,justify='center',state="readonly")
    cityChoose = 0
    cityOption.current(cityChoose)
    cityOption.grid(row = 1, column=1)

    cityLabel = Label(weatherCity, text="")
    cityLabel.grid(row = 3,column=1, pady = 5)

    Button(weatherCity, text="Submit", width=15, height=1, command=lambda: sendCityWeatherThread(cityOption.get(),cityLabel)).grid(row=2,column=1, pady=(15,5))

def showWeatherByDate():
    Button(weatherDate, text="< Back", width=8, height=1, command=lambda: back(weatherDate, mainMenuFrame)).grid(row = 0, column=0)
    Label(weatherDate, text = "WEATHER DATA").grid(row=0,column=1,sticky="WE",pady=20)

    #Day
    dayList = list(range(32))

    Label(weatherDate, text = "Choose day").grid(pady=5,row=1, column=0, sticky="W", padx=(30,5))
    dayChoose = StringVar(weatherDate)
    dayOption = ttk.Combobox(weatherDate, textvariable=dayChoose, values=dayList,width=10,state="readonly")
    dayChoose = dayList.index(DAY)
    dayOption.current(dayChoose)
    dayOption.grid(row = 1, column=1)

    #Month
    monthList = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "Setemper", "October", "November", "December"]

    Label(weatherDate, text = "Choose Month").grid(pady=5,row=2, column=0, sticky="W", padx=(30,5))
    monthChoose = StringVar(weatherDate)
    monthOption = ttk.Combobox(weatherDate, textvariable=monthChoose, value=monthList,width=10,state="readonly")
    monthChoose = monthList.index(MONTH)
    monthOption.current(monthChoose)
    monthOption.grid(row = 2, column=1)

    #Year
    yearList = ["2020","2021","2022"]

    Label(weatherDate, text = "Choose Year").grid(pady=5,row=3, column=0, sticky="W", padx=(30,5))
    yearChoose = StringVar(weatherDate)
    yearOption = ttk.Combobox(weatherDate, textvariable = yearChoose, values=yearList,width=10,state="readonly")
    yearChoose = yearList.index(YEAR)
    yearOption.current(yearChoose)
    yearOption.grid(row = 3, column=1)

    myLabel = Label(weatherDate, text="")
    myLabel.grid(row = 5,column=1, pady = 5)

    Button(weatherDate, text="Submit", width=10, height=1, command=lambda: sendAllWeathersThread(dayOption.get(),monthOption.get(),yearOption.get(),myLabel )).grid(row=4,column=1,pady=(15,5))

# client functions
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
def back(thisFrame, nextFrame):
    for child in thisFrame.winfo_children():
        child.destroy()
    showFrame(nextFrame)

def connectServer(entry):
    global client # client socket
    host = entry.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddr = (host, PORT)
    try:
        client.connect(serverAddr)
        print('Connected to server: ' + str(serverAddr))
        showFrame(signInFrame)
    except:
        print("Could not find server's IP or request timeout")
        messagebox.showerror("Error", "Could not find server's IP or request timeout")
def sendUserInfo(usernameEntry, passwordEntry, type):
    username = usernameEntry.get()
    usernameEntry.delete(0, 'end')
    password = passwordEntry.get()
    passwordEntry.delete(0, 'end')
    if(send(type + " " + username + " " + password)):
        serverResponse = receive()
        frameManager(serverResponse)

def sendAllWeathers(day,month, year, myLabel):
    datetime = day + " " + month + " " + year
    message = "/list %s" % datetime
    send(message)
    data = receive()

    data = ("[Date: %s]\n" % (datetime)) + data
    myLabel['text'] = data

def sendCityWeather(city,label):
    message = "/city %s" % (city)
    send(message)
    data = receive()

    data = ("[%s]\n" % (city)) + data
    label['text'] = data

# Thread function
def disconnectThread():
    threadDisconnect = Thread(target=disconnectServer)
    threadDisconnect.daemon = True
    threadDisconnect.start()

def connectThread(entry):
    threadConnect = Thread(target=connectServer, args=(entry,))
    threadConnect.daemon = True
    threadConnect.start()


def sendUserInfoThread(usernameEntry, passwordEntry, type):
    threadSend = Thread(target=sendUserInfo, args=(usernameEntry, passwordEntry, type,))
    threadSend.daemon = True
    threadSend.start()

def sendAllWeathersThread(day,month, year, myLabel):
    threadSendWeather = Thread(target=sendAllWeathers, args=(day,month, year, myLabel,))
    threadSendWeather.daemon = True
    threadSendWeather.start()
def sendCityWeatherThread(city,label):

    thread = Thread(target=sendCityWeather, args=(city, label,))
    thread.daemon = True
    thread.start()

# main functions
if __name__ == "__main__":
    today = date.today()
    DAY = int(today.strftime("%d"))
    MONTH = today.strftime("%B")
    YEAR = today.strftime("%Y")

    PORT = 65432
    root = Tk()
    root.geometry("400x400")
    root.title("Weathery App")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    chooseSVFrame = Frame(root)
    signInFrame = Frame(root)
    signUpFrame = Frame(root)
    mainMenuFrame = Frame(root)
    weatherDate = Frame(root)
    weatherCity = Frame(root)

    for frame in (chooseSVFrame, signInFrame, signUpFrame, mainMenuFrame, weatherDate,weatherCity):
        frame.grid(row=0, column=0, sticky='nsew')

    setUpChooseSVFrame()
    setUpSignInFrame()
    setUpSignUpFrame()
    setUpMainMenuFrame()
    showWeatherByDate()


    Thread(target=showFrame, args=(chooseSVFrame,)).start()
    root.protocol("WM_DELETE_WINDOW", exitApp) # handle when click "X" on tkinter app
    root.mainloop()

    root.mainloop()



