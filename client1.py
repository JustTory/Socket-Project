import socket
HOST = input('Server IP: ')
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddr = (HOST, PORT)
s.connect(serverAddr)
print('Connected to server: ' + str(serverAddr))

while True:
    serverResponse = s.recv(1024)
    print('Server:', serverResponse.decode("utf8"))

    while True:
        clientMsg = input('\nClient: ')
        s.sendall(bytes(clientMsg, "utf8"))
        if clientMsg == "/exit": break
        data = s.recv(1024)
        print('Server:', data.decode("utf8"))
s.close()
