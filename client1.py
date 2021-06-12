import socket
from tkinter import *
from tkinter import messagebox

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

def sendUserInfo(usernameEntry, passwordEntry, type):
    username = usernameEntry.get()
    usernameEntry.delete(0, 'end')
    password = passwordEntry.get()
    passwordEntry.delete(0, 'end')

    send(type + " " + username + " " + password)
    serverResponse = receive()
    frameManager(serverResponse)

def showFrame(frame):
    frame.tkraise()

def setUpChooseSVFrame():
    Label(chooseSVFrame, text="Input server's IP").pack()
    serverIPEntry = Entry(chooseSVFrame)
    serverIPEntry.pack()
    Button(chooseSVFrame, text="Select", height="1", width="10", command=lambda: connectServer(serverIPEntry)).pack()

def setUpSignInFrame():
    Label(signInFrame, text="SIGN IN").pack()
    Label(signInFrame, text="Username").pack()
    usernameEntry = Entry(signInFrame)
    usernameEntry.pack()
    Label(signInFrame, text="Password").pack()
    passwordEntry = Entry(signInFrame, show= '*')
    passwordEntry.pack()
    Button(signInFrame, text="Login", width=10, height=1, command=lambda: sendUserInfo(usernameEntry, passwordEntry, "signin")).pack()
    Button(signInFrame, text="Don't have an account? Sign up", width=30, height=1, command=lambda: showFrame(signUpFrame)).pack()

def setUpSignUpFrame():
    Label(signUpFrame, text="CREATE ACCOUNT").pack()
    Label(signUpFrame, text="Username").pack()
    usernameEntry = Entry(signUpFrame)
    usernameEntry.pack()
    Label(signUpFrame, text="Password").pack()
    passwordEntry = Entry(signUpFrame, show= '*')
    passwordEntry.pack()
    Button(signUpFrame, text="Create account", width=15, height=1, command=lambda: sendUserInfo(usernameEntry, passwordEntry, "signup")).pack()
    Button(signUpFrame, text="Already have an account? Sign in", width=30, height=1, command=lambda: showFrame(signInFrame)).pack()

def setUpMainMenuFrame():
    Label(mainMenuFrame, text="MAIN MENU").pack()
    Button(mainMenuFrame, text="List all cities", width=15, height=1).pack()
    Button(mainMenuFrame, text="Select a city", width=15, height=1).pack()

def connectServer(entry, port = 65432):
    host = entry.get()
    serverAddr = (host, port)
    try:
        s.connect(serverAddr)
        print('Connected to server: ' + str(serverAddr))
        showFrame(signInFrame)
    except:
        print("Could not find server's IP or request timeout")
        messagebox.showerror("Error", "Could not find server's IP or request timeout")


root = Tk()
root.geometry("400x400")
root.title("Weathery App")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

chooseSVFrame = Frame(root)
signInFrame = Frame(root)
signUpFrame = Frame(root)
mainMenuFrame = Frame(root)

for frame in (chooseSVFrame, signInFrame, signUpFrame, mainMenuFrame):
    frame.grid(row=0, column=0, sticky='nsew')

setUpChooseSVFrame()
setUpSignInFrame()
setUpSignUpFrame()
setUpMainMenuFrame()

#receiveMsgList = {}

showFrame(chooseSVFrame)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

root.mainloop()



