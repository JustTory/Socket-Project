import socket
HOST = input('Server IP: ')
PORT = 65432 # server's port: any non-privileged ports

# s = socket.socket(addr_family, type)
# addr_family:
#   socket.AF_INET: Internet protocol (IPv4)
#   socket.AF_INET6: Internet protocol (IPv6)
# type:
#   socket.SOCK_STREAM: Connection based stream (TCP)
#   socket.SOCK_DGRAM: Datagrams (UDP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddr = (HOST, PORT)
s.connect(serverAddr)
print('Connected to server: ' + str(serverAddr))

while True:
    serverResponse = s.recv(1024)

while True:
    clientMsg = input('\nClient: ')
    s.sendall(bytes(clientMsg, "utf8"))
    if clientMsg == "/exit": break
    data = s.recv(1024)
    print('Server:', data.decode("utf8"))

s.close()
