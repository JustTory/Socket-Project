import socket
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from datetime import date
import calendar

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

def onDateChange(dayOption, dayChoose,monthOption, yearOption):
    newdayChoose = dayOption.get()
    monthChoose = monthOption.get()
    yearChoose = yearOption.get()


    day = int(newdayChoose)
    month = monthList.index(monthChoose) + 1
    year = int(yearChoose)

    dayMargin = calendar.monthrange(year,month)[1]

    if ( day > dayMargin ):
        dayChoose = dayMargin-1
        dayOption.current(dayChoose)

    dayList = list(range(1, dayMargin+1))
    dayOption['values'] = dayList


def showFrame(frame):
    frame.tkraise()

# frame functions
def setUpChooseSVFrame():
    Label(chooseSVFrame, text="Server's IP", font = LABELFONT, bg='white').pack(pady=(60,30))
    serverIPEntry = Entry(chooseSVFrame, width=25, font = FONT, highlightthickness=1, highlightbackground = "black", bd=0)
    serverIPEntry.pack(ipady=5)
    serverIPEntry.focus()

    Button(chooseSVFrame, text="Connect", height="1", width="10", font = FONT, fg='white', bg='#0275d8', bd=0, command=lambda:connectThread(serverIPEntry)).pack(pady=20)

def setUpSignInFrame():
    Button(signInFrame, text="Disconnect", width=11, height=1, font = FONT, fg='white', bg='#d9534f', bd=0, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(signInFrame, text="Sign In", font = LABELFONT, bg='white').pack(pady=(30,40))
    Label(signInFrame, text="Username", font = FONT, bg='white').pack()
    usernameEntry = Entry(signInFrame, width=25, font = FONT, highlightthickness=1, highlightbackground = "black", bd=0)
    usernameEntry.pack(ipady=5)

    Label(signInFrame, text="Password", font = FONT, bg='white').pack(pady=(20,0))
    passwordEntry = Entry(signInFrame, show= '*', width=25, font = FONT, highlightthickness=1, highlightbackground = "black", bd=0)
    passwordEntry.pack(ipady=5)

    Button(signInFrame, text="Login", width=10, height=1, font = FONT, fg='white', bg='#0275d8', bd=0, command=lambda: sendUserInfoThread(usernameEntry, passwordEntry, "signin")).pack(pady=(30,20))
    Button(signInFrame, text="Don't have an account? Sign Up", width=30, height=1, font = FONT, fg='black', bg='#f7f7f7', bd=0, command=lambda: showFrame(signUpFrame)).pack()

def setUpSignUpFrame():
    Button(signUpFrame, text="Disconnect", width=11, height=1, font = FONT, fg='white', bg='#d9534f', bd=0, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(signUpFrame, text="Create Account", font = LABELFONT, bg='white').pack(pady=(30,40))
    Label(signUpFrame, text="Username", font = FONT, bg='white').pack()
    usernameEntry = Entry(signUpFrame, width=25, font = FONT, highlightthickness=1, highlightbackground = "black", bd=0)
    usernameEntry.pack(ipady=5)

    Label(signUpFrame, text="Password", font = FONT, bg='white').pack(pady=(20,0))
    passwordEntry = Entry(signUpFrame, show= '*', width=25, font = FONT, highlightthickness=1, highlightbackground = "black", bd=0)
    passwordEntry.pack(ipady=5)

    Button(signUpFrame, text="Create account", width=15, height=1, font = FONT, fg='white', bg='#0275d8', bd=0, command=lambda: sendUserInfoThread(usernameEntry, passwordEntry, "signup")).pack(pady=(30,20))
    Button(signUpFrame, text="Already have an account? Sign In", width=30, height=1, font = FONT, fg='black', bg='#f7f7f7', bd=0, command=lambda: showFrame(signInFrame)).pack()

def setUpMainMenuFrame():
    Button(mainMenuFrame, text="Disconnect", width=11, height=1, font = FONT, fg='white', bg='#d9534f', bd=0, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(mainMenuFrame, text="Main Menu", font = LABELFONT, bg='white').pack(pady=(30,40))
    Button(mainMenuFrame, text="View weather by date", width=25, height=2, font = FONT, fg='white', bg='#0275d8', bd=0, command=lambda: showFrame(weatherDate)).pack(pady=(0,20))
    Button(mainMenuFrame, text="View weather by city", width=25, height=2, font = FONT, fg='white', bg='#0275d8', bd=0, command=lambda: getAllCity()).pack()

def getAllCity():
    # get City JSON
    send("/getCity")
    global cityList
    cityList = receive()
    cityList = cityList.split("\n")

    setUpWeatherByCity()
    showFrame(weatherCity)
def setUpWeatherByCity():
    Button(weatherCity, text="< Back", width=8, height=1, font = FONT, fg='black', bg='#f7f7f7', bd=0, command=lambda: back(weatherCity, mainMenuFrame)).grid(row = 0, column=0, sticky="NW")
    Label(weatherCity, text = "City Data", font = LABELFONT, bg='white').grid(row=0,column=1,sticky="WE",pady=50)

    Label(weatherCity, text = "Choose city", font = FONT, bg='white').grid(pady=5,row=1, column=0, sticky="W", padx=(155,5))
    cityChoose = StringVar(weatherCity)
    cityOption = ttk.Combobox(weatherCity, textvariable=cityChoose,values=cityList,width=20,justify='center',state="readonly",font = FONT)
    cityChoose = 0
    cityOption.current(cityChoose)
    cityOption.grid(row = 1, column=1, ipady= 5)

    cityLabel = Label(weatherCity, text="", font = FONT, bg='white')
    cityLabel.grid(row = 3,column=1, pady = 5)

    Button(weatherCity, text="Submit", width=15, height=1, font = FONT, fg='white', bg='#0275d8', bd=0, command=lambda: sendCityWeatherThread(cityOption.get(),cityLabel)).grid(row=2,column=1, pady=(25,30))

def setUpWeatherByDate():
    Button(weatherDate, text="< Back", width=8, height=1, font = FONT, fg='black', bg='#f7f7f7', bd=0, command=lambda: back(weatherDate, mainMenuFrame)).grid(row = 0, column=0, sticky="NW")
    Label(weatherDate, text = "Weather Data", font = LABELFONT, bg='white').grid(row=0,column=1,sticky="WE",pady=50)

    #Day
    dayList = list(range(1, 32))
    Label(weatherDate, text = "Day", font = FONT, bg='white').grid(pady=15,row=1, column=0, sticky="W", padx=(170,5) )
    dayChoose = StringVar(weatherDate)
    dayOption = ttk.Combobox(weatherDate, textvariable=dayChoose, values=dayList,width=20,state="readonly", justify='center',font = FONT)
    dayChoose = dayList.index(DAY)
    dayOption.current(dayChoose)
    dayOption.grid(row = 1, column=1, ipady= 5)

    #Month
    global monthList
    monthList = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "Setemper", "October", "November", "December"]
    Label(weatherDate, text = "Month", font = FONT, bg='white').grid(pady=15,row=2, column=0, sticky="W", padx=(170,5))
    monthChoose = StringVar(weatherDate)
    monthOption = ttk.Combobox(weatherDate, textvariable=monthChoose, value=monthList,width=20,state="readonly", justify='center',font = FONT)
    monthChoose = monthList.index(MONTH)
    monthOption.current(monthChoose)
    monthOption.bind("<<ComboboxSelected>>",lambda event: onDateChange(dayOption,dayChoose,monthOption,yearOption))
    monthOption.grid(row = 2, column=1, ipady= 5)

    #Year
    global yearList
    yearList = ["2020","2021","2022"]
    yearChoose = StringVar(weatherDate)
    Label(weatherDate, text = "Year", font = FONT, bg='white').grid(pady=15,row=3, column=0, sticky="W", padx=(170,5))
    yearChoose = yearList.index(YEAR)
    yearOption = ttk.Combobox(weatherDate, textvariable = yearChoose, values=yearList,width=20,state="readonly", justify='center',font = FONT)
    yearOption.current(yearChoose)
    yearOption.bind("<<ComboboxSelected>>", lambda event:onDateChange(dayOption,dayChoose,monthOption,yearOption))
    yearOption.grid(row = 3, column=1, ipady= 5)

    myLabel = Label(weatherDate, text="", font = FONT, bg='white')
    myLabel.grid(row = 5,column=1, pady = 5)

    dayMargin = calendar.monthrange(int(YEAR), monthChoose)[1]
    dayOption['values'] = list(range(1, dayMargin))

    Button(weatherDate, text="Submit", width=15, height=1, font = FONT, fg='white', bg='#0275d8', bd=0, command=lambda: sendAllWeathersThread(dayOption.get(),monthOption.get(),yearOption.get(),myLabel )).grid(row=4,column=1,pady=(25,30))

# client functions
def disconnectServer():
    global client
    send("exit")
    client.close()
    del client
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

    setUpWeatherByDate()
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
        del client
def sendUserInfo(usernameEntry, passwordEntry, type):
    username = usernameEntry.get()
    usernameEntry.delete(0, 'end')
    password = passwordEntry.get()
    passwordEntry.delete(0, 'end')
    if(send(type + " " + username + " " + password)):
        serverResponse = receive()

        if (type == "signin"):
            if (serverResponse == "success"):
                showFrame(mainMenuFrame)
                messagebox.showinfo("Success", "You have signed in successfully")
            elif (serverResponse == "fail"):
                messagebox.showerror("Error", "Incorrect username or password")

        else:
            if (serverResponse == "success"):
                messagebox.showinfo("Success", "You have created an account successfully")
                showFrame(mainMenuFrame)
            elif (serverResponse == "fail"):
                messagebox.showerror("Error", "Username already exists")

        if (serverResponse == "syntax"):
            messagebox.showerror("Error", "Username or password can't be empty")



def showAllWeathers(day,month, year, myLabel):
    datetime = day + " " + month + " " + year
    message = "/list %s" % datetime
    if (send(message)):
        data = receive()

        data = ("[Date: %s]\n" % (datetime)) + data
        myLabel['text'] = data

def showCityWeather(city,label):
    city = city.replace(" ","")
    message = "/city %s" % (city)
    if (send(message)):
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
    threadSendWeather = Thread(target=showAllWeathers, args=(day,month, year, myLabel,))
    threadSendWeather.daemon = True
    threadSendWeather.start()
def sendCityWeatherThread(city,label):
    thread = Thread(target=showCityWeather, args=(city, label,))
    thread.daemon = True
    thread.start()

# main functions
if __name__ == "__main__":
    today = date.today()
    DAY = int(today.strftime("%d"))
    MONTH = today.strftime("%B")
    YEAR = today.strftime("%Y")

    PORT = 65432

    FONT = ("Tahoma", 14)
    LABELFONT = ("Tahoma", 20, "bold")

    root = Tk()
    root.geometry("700x800")
    root.title("Weathery - Client")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    chooseSVFrame = Frame(root, bg='white')
    signInFrame = Frame(root, bg='white')
    signUpFrame = Frame(root, bg='white')
    mainMenuFrame = Frame(root, bg='white')
    weatherDate = Frame(root, bg='white')
    weatherCity = Frame(root, bg='white')

    for frame in (chooseSVFrame, signInFrame, signUpFrame, mainMenuFrame, weatherDate,weatherCity):
        frame.grid(row=0, column=0, sticky='nsew')

    setUpChooseSVFrame()
    setUpSignInFrame()
    setUpSignUpFrame()
    setUpMainMenuFrame()
    setUpWeatherByDate()


    Thread(target=showFrame, args=(chooseSVFrame,)).start()
    root.protocol("WM_DELETE_WINDOW", exitApp) # handle when click "X" on tkinter app
    root.mainloop()



