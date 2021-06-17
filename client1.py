import socket
from tkinter import *
from tkinter import messagebox
from threading import Thread


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
        messagebox.showinfo("Success", "You have signed in successfully")
        showFrame(mainMenuFrame)
    elif (serverResponse == "SIGN IN: info incorrect"):
        messagebox.showerror("Error", "Incorrect username or password")
    elif (serverResponse == "SIGN IN: syntax error"):
        messagebox.showerror("Error", "Username or password can't be empty")

    elif (serverResponse == "SIGN UP: success"):
        messagebox.showinfo("Success", "You have created an account successfully")
        showFrame(mainMenuFrame)
    elif (serverResponse == "SIGN UP: username already existed"):
        messagebox.showerror("Error", "Username already existed")
    elif (serverResponse == "SIGN UP: syntax error"):
        messagebox.showerror("Error", "Username or password can't be empty")

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
    Label(signInFrame, text="Username").pack()
    usernameEntry = Entry(signInFrame)
    #usernameEntry.bind("<Return>", (lambda event: sendUserInfoThread(usernameEntry, passwordEntry, "signin")))
    usernameEntry.pack()
    usernameEntry.focus()

    Label(signInFrame, text="Password").pack(pady=(10,0))
    passwordEntry = Entry(signInFrame, show= '*')
    passwordEntry.bind("<Return>", (lambda event: sendUserInfoThread(usernameEntry, passwordEntry, "signin")))
    passwordEntry.pack()

    Button(signInFrame, text="Login", width=10, height=1, command=lambda: sendUserInfoThread(usernameEntry, passwordEntry, "signin")).pack(pady=(20,10))
    Button(signInFrame, text="Don't have an account? Sign up", width=30, height=1, command=lambda: showFrame(signUpFrame)).pack()

def setUpSignUpFrame():
    Button(signUpFrame, text="< Disconnect", width=10, height=1, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(signUpFrame, text="CREATE ACCOUNT").pack(pady=20)
    Label(signUpFrame, text="Username").pack()
    usernameEntry = Entry(signUpFrame)
    #usernameEntry.bind("<Return>", (lambda event: sendUserInfoThread(usernameEntry, passwordEntry, "signup")))
    usernameEntry.pack()

    Label(signUpFrame, text="Password").pack(pady=(10,0))
    passwordEntry = Entry(signUpFrame, show= '*')
    #passwordEntry.bind("<Return>", (lambda event: sendUserInfoThread(usernameEntry, passwordEntry, "signup")))
    passwordEntry.pack()

    Button(signUpFrame, text="Create account", width=15, height=1, command=lambda: sendUserInfoThread(usernameEntry, passwordEntry, "signup")).pack(pady=(20,10))
    Button(signUpFrame, text="Already have an account? Sign in", width=30, height=1, command=lambda: showFrame(signInFrame)).pack()

def setUpMainMenuFrame():
    Button(mainMenuFrame, text="< Disconnect", width=10, height=1, command=lambda: disconnectThread()).pack(side=TOP, anchor=NW)
    Label(mainMenuFrame, text="MAIN MENU").pack(pady=20)
    Button(mainMenuFrame, text="List all cities", width=15, height=1).pack(pady=(0,10))
    Button(mainMenuFrame, text="Select a city", width=15, height=1).pack()

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
    serverAddr = (host, PORT)
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

    if(send(type + " " + username + " " + password)):
        serverResponse = receive()
        frameManager(serverResponse)


# main function
if __name__ == "__main__":
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

    for frame in (chooseSVFrame, signInFrame, signUpFrame, mainMenuFrame):
        frame.grid(row=0, column=0, sticky='nsew')

    setUpChooseSVFrame()
    setUpSignInFrame()
    setUpSignUpFrame()
    setUpMainMenuFrame()

    Thread(target=showFrame, args=(chooseSVFrame,)).start()

    root.protocol("WM_DELETE_WINDOW", exitApp) # handle when click "X" on tkinter app
    root.mainloop()





