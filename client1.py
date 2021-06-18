import socket
from tkinter import *
from tkinter import ttk
# from tkinter.ttk import Progressbar
from tkinter import messagebox
from threading import Thread
from datetime import date
import json

today = date.today()
DAY = int(today.strftime("%d"))
MONTH = today.strftime("%B")
YEAR = today.strftime("%Y")

cityJson = open("cities.json")
cityData = json.load(cityJson)['cities']


def send(msg):
    s.sendall(bytes(msg, "utf8"))

def receive():
    msg = s.recv(1024).decode("utf8")
    return msg

def frameManager(serverResponse):
    print(serverResponse)
    if (serverResponse == "sign in success"):
        messagebox.showinfo("Success", "You have signed in successfully")
        showFrame(mainMenuFrame)
    elif (serverResponse == "sign up success"):
        messagebox.showinfo("Success", "You have created an account successfully")
        showFrame(mainMenuFrame)
    elif (serverResponse == "info incorrect"):
        messagebox.showerror("Error", "Incorrect username or password")
    elif (serverResponse == "username exists"):
        messagebox.showerror("Error", "Username already exists")
    elif (serverResponse == "syntax error"):
        messagebox.showerror("Error", "Username or password can't be empty")

def showFrame(frame):
    frame.tkraise()

# def setUpPBFrame():
#     progressBar = Progressbar(root, orient='horizontal', mode='indeterminate', length=200)
#     progressBar.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
#     progressBar.start()

def setUpChooseSVFrame():
    Label(chooseSVFrame, text="SERVER IP").pack(pady=20)
    Label(chooseSVFrame, text="Input server's IP").pack()
    serverIPEntry = Entry(chooseSVFrame)
    serverIPEntry.bind("<Return>", (lambda event: connectThread(serverIPEntry)))
    serverIPEntry.pack()
    serverIPEntry.focus()

    Button(chooseSVFrame, text="Select", height="1", width="10", command=lambda:connectThread(serverIPEntry)).pack(pady=10)

def setUpSignInFrame():
    Label(signInFrame, text="SIGN IN").pack(pady=20)
    Label(signInFrame, text="Username").pack()
    usernameEntry = Entry(signInFrame)
    usernameEntry.bind("<Return>", (lambda event: sendUserInfo(usernameEntry, passwordEntry, "signin")))
    usernameEntry.pack()

    Label(signInFrame, text="Password").pack(pady=(10,0))
    passwordEntry = Entry(signInFrame, show= '*')
    passwordEntry.bind("<Return>", (lambda event: sendUserInfo(usernameEntry, passwordEntry, "signin")))
    passwordEntry.pack()


    Button(signInFrame, text="Login", width=10, height=1, command=lambda: sendUserInfo(usernameEntry, passwordEntry, "signin")).pack(pady=(20,10))
    Button(signInFrame, text="Don't have an account? Sign up", width=30, height=1, command=lambda: showFrame(signUpFrame)).pack()

def setUpSignUpFrame():
    Label(signUpFrame, text="CREATE ACCOUNT").pack(pady=20)
    Label(signUpFrame, text="Username").pack()
    usernameEntry = Entry(signUpFrame)
    usernameEntry.pack()

    Label(signUpFrame, text="Password").pack(pady=(10,0))
    passwordEntry = Entry(signUpFrame, show= '*')
    passwordEntry.pack()

    Button(signUpFrame, text="Create account", width=15, height=1, command=lambda: sendUserInfo(usernameEntry, passwordEntry, "signup")).pack(pady=(20,10))
    Button(signUpFrame, text="Already have an account? Sign in", width=30, height=1, command=lambda: showFrame(signInFrame)).pack()

def sendAllWeathers(day,month, year, myLabel): 
    datetime = day + " " + month + " " + year
    message = "/list %s" % datetime
    send(message)
    data = receive()
    
    data = ("[Date: %s]\n" % (datetime)) + data
    myLabel['text'] = data
    # Label(weatherDate, text=queryRes).grid(row=4,column=1,padx=30)
def showWeatherByDate():
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

    Button(weatherDate, text="Submit", width=10, height=1, command=lambda: sendAllWeathers(dayOption.get(),monthOption.get(),yearOption.get(),myLabel )).grid(row=4,column=1,pady=(15,5))

def sendCityWeather(city,label):
    message = "/city %s" % (city)
    send(message)
    data = receive()
    
    data = ("[%s]\n" % (city)) + data
    label['text'] = data
def showWeatherByCity():
    Label(weatherCity, text = "CITY DATA").grid(row=0,column=1,sticky="WE",pady=20)

    cityList= list(cityData)

    Label(weatherCity, text = "Choose a city").grid(pady=5,row=1, column=0, sticky="W", padx=(30,5))
    cityChoose = StringVar(weatherCity)
    cityOption = ttk.Combobox(weatherCity, textvariable=cityChoose,values=cityList,width=15,justify='center',state="readonly")
    cityChoose = 0
    cityOption.current(cityChoose)
    cityOption.grid(row = 1, column=1)

    cityLabel = Label(weatherCity, text="")
    cityLabel.grid(row = 3,column=1, pady = 5)

    Button(weatherCity, text="Submit", width=15, height=1, command=lambda: sendCityWeather(cityOption.get(),cityLabel)).grid(row=2,column=1, pady=(15,5))


def setUpMainMenuFrame():
    Label(mainMenuFrame, text="MAIN MENU").pack()
    Button(mainMenuFrame, text="List all cities", width=15, height=1, command=lambda: showFrame(weatherDate)).pack()
    Button(mainMenuFrame, text="Select a city", width=15, height=1, command=lambda: showFrame(weatherCity)).pack()

def connectThread(entry):
    # global threadConnect
    threadConnect = Thread(target=connectServer, args=(entry,))
    threadConnect.daemon = True
    threadConnect.start()
    # chooseSVFrame.after(100, lambda: checkThreadStatus(threadConnect))

# def checkThreadStatus(thread, frame):
#     if thread.is_alive() == False:
#         frame.grid_forget()
#     else
#         checkThreadStatus(thread)

def connectServer(entry):
    host = entry.get()
    serverAddr = (host, PORT)
    try:
        s.connect(serverAddr)
        print('Connected to server: ' + str(serverAddr))
        showFrame(signInFrame)
    except:
        print("Could not find server's IP or request timeout")
        messagebox.showerror("Error", "Could not find server's IP or request timeout")

# def sendUserInfoThread(usernameEntry, passwordEntry, type):
#     threadSend = Thread(target=sendUserInfo, args=(usernameEntry, passwordEntry, type,))
#     threadSend.daemon = True
#     threadSend.start()

def sendUserInfo(usernameEntry, passwordEntry, type):
    username = usernameEntry.get()
    usernameEntry.delete(0, 'end')
    password = passwordEntry.get()
    passwordEntry.delete(0, 'end')

    send(type + " " + username + " " + password)
    serverResponse = receive()
    frameManager(serverResponse)

PORT = 65432
root = Tk()
root.geometry("400x400")
root.title("Weathery App")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

pbFrame = Frame(root)
chooseSVFrame = Frame(root)
signInFrame = Frame(root)
signUpFrame = Frame(root)
mainMenuFrame = Frame(root)
weatherDate = Frame(root)
weatherCity = Frame(root)

for frame in (pbFrame, chooseSVFrame, signInFrame, signUpFrame, mainMenuFrame, weatherDate,weatherCity):
    frame.grid(row=0, column=0, sticky='nsew')

# setUpPBFrame()
setUpChooseSVFrame()
setUpSignInFrame()
setUpSignUpFrame()
setUpMainMenuFrame()
showWeatherByDate()
showWeatherByCity()
#receiveMsgList = {}

Thread(target=showFrame, args=(chooseSVFrame,)).start()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root.mainloop()



